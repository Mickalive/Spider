# EXP-PRODUCT-35476271728 — preregistration

**Experiment ID:** EXP-PRODUCT-35476271728
**Lane:** product
**Claim:** C-FRESHNESS
**Created:** 2026-09-19T23:30:05.959120+00:00
**Parent:** EXP-PRODUCT-35456068953 (handoff sha256: 1f9e9cdc48847a0a6ca2a7799f35e77e1ac599a2e0f6e33fdaeaa3e6e492fcfb)

---

## 1. Question

At n>=480, does token_refresh behavioral detection survive co-occurring structural noise with TOST equivalence confirmed at delta=0.15, and how does detection threshold choice affect TP/FP tradeoff?

## 2. Hypothesis

Token_refresh behavioral detection (TP >= 0.85) and behavioral variance (std > 0.05) will survive at n=480 under co-occurring structural noise, and TOST equivalence at delta=0.15 will be confirmed (CI upper bound < 0.15), resolving the parent's TOST lower-tail failure (p_lower=0.081, ci_lower=-0.185) as a sample-size power artifact. Additionally, the threshold sensitivity analysis will reveal whether the 0.25 threshold tautology (below both bimodal modes 0.35/0.65) limits discriminating power.

## 3. Falsification criteria

FALSIFIED if any of:
- (F1) token_refresh TP < 0.85 under co-occurring noise at n=480
- (F2) behavioral_std < 0.05 under stochastic drift at n=480
- (F3) structural discrimination < 0.5 (positive control fails)
- (F4) FP > 0.15 on noise-only samples
- (F5) TOST at delta=0.15 still fails (CI upper bound >= 0.15) at n=480

MIXED if C1-C4 pass but TOST lower tail still fails at n=480 (equivalence not confirmed despite adequate power, indicating genuine non-equivalence rather than sample-size artifact).

## 4. Baselines

| ID | Description | Expected |
|----|-------------|----------|
| B-N240-PARENT | Parent n=240: TP=1.0, std 0.134-0.143, r=-0.060, TOST p_lower=0.081 | n=480 narrows CI so TOST lower tail passes |
| B-N480-MOCK-ORTHOGONALITY | Three prior n=480 mock experiments: r in [-0.026, 0.046], CI upper in [0.064, 0.135], all TOST PASS | Token_refresh orthogonality consistent with prior experiments |
| B-TOKEN-REFRESH-N240 | Token_refresh TP=1.0 at n=240 under co-occurring noise | TP >= 0.85 at n=480 |

## 5. Controls

### Positive control: PC-STRUCTURAL-DISCRIMINATION
HTTP fingerprint full-vector discrimination on stochastic Flask+SQLite mock server with 4 auth states. Expected: discrimination > 0.5. Replicates EXP-RUNTIME-33902315583 and EXP-PRODUCT-35445596342.

### Null control: NC-NOISE-FP
Behavioral false positive rate on 240 structural noise-only samples (4 noise types x 60 samples). Expected: FP <= 0.15. All noise types are orthogonal to auth drift (optional_field_addition, description_change, response_time_jitter, field_type_normalization).

### Variance controls
- C2-VARIANCE: All 4 co-occurring conditions must have behavioral_std > 0.05 at n=480
- CTL-STOCHASTIC-TOKEN-REFRESH: p_refresh_success=0.7 produces bimodal scores with std > 0.05

## 6. Measurement validity

1. Stochastic Flask+SQLite mock server matching EXP-PRODUCT-35456068953: Flask 3.1.3 + SQLite WAL-mode DB + in-memory cache TTL=0.5s + jitter 10-100ms + mixed JWT algorithms (HS256/RS256)
2. Token_refresh drift: p_refresh_success=0.7 (Bernoulli), producing bimodal behavioral scores (~0.35 on failure, ~0.65 on success)
3. Server state fully reset between conditions: set_drift(None) clears all state before each phase
4. N = 480 paired samples minimum (60 per condition x 8 co-occurring conditions) for token_refresh TP and orthogonality; additional 240 noise-only samples for FP measurement
5. Orthogonality tested via TOST equivalence test at delta=0.15 on Fisher-z transformed Pearson correlation
6. All measurements on localhost mock server (127.0.0.1:18951), not production APIs
7. This experiment does NOT make real LLM calls
8. Global RNG seeded at 42 before server thread start; server runs threaded=False, client is sequential

## 7. Decision rule

SURVIVES_CURRENT_TEST requires ALL of:
- (C1) Structural discrimination > 0.5 (positive control)
- (C2) Token_refresh TP >= 0.85 under co-occurring noise at n=480
- (C3) Token_refresh behavioral_std > 0.05 under stochastic drift at n=480
- (C4) FP <= 0.15 on noise-only samples
- (C5) TOST equivalence at delta=0.15 (CI upper bound < 0.15)

FALSIFIED if any condition fails.

MIXED if C1-C4 pass but C5 fails (TOST lower tail still fails at n=480, indicating genuine non-equivalence rather than power artifact).

## 8. Experimental phases

### Phase A: Structural discrimination probe (40 requests)
Probe /api/data endpoint 10x per auth state on the stochastic server. Measure full-vector HTTP fingerprint discrimination across 4 states. Verify 3 unique fingerprints (expired/invalid collision). Duration: ~2 minutes.

### Phase B: Co-occurring noise paired samples (480 paired requests)
480 paired samples across 4 co-occurring conditions (token_refresh x 4 structural noises, 120 samples each). Each sample reads behavioral signal from /api/session/status and structural signal from /api/schema over real HTTP. Duration: ~15-20 minutes.

### Phase C: Noise-only samples (240 requests)
240 noise-only samples (4 noise types x 60) with NO drift active. Measure behavioral FP rate. Duration: ~8-10 minutes.

### Phase D: Isolated token_refresh TP (60 requests)
60 isolated token_refresh samples with stochastic drift (p_refresh_success=0.7). Measure TP, behavioral_mean, behavioral_std. Duration: ~2-3 minutes.

### Phase E: Threshold sensitivity analysis (48 requests)
48 threshold-probe samples (8 samples at 6 threshold values: 0.15, 0.20, 0.25, 0.30, 0.35, 0.40). For each threshold, measure TP, FP, and detection count. Uses Phase B and C data. Duration: ~1-2 minutes.

**Total estimated runtime:** 35-45 minutes.

## 9. Threshold sensitivity analysis (exploratory)

At each of 6 threshold values {0.15, 0.20, 0.25, 0.30, 0.35, 0.40}, compute:
- TP rate on token_refresh drift samples (Phase B + D combined)
- FP rate on noise-only samples (Phase C)
- Detection count (samples at/above threshold)

This analysis is EXPLORATORY and does not affect the primary SURVIVES/FALSIFIED decision. It informs future threshold calibration and addresses audit finding V3 (threshold tautology).

## 10. Expected information gain

HIGH: directly resolves two audit findings simultaneously:
1. TOST lower-tail failure at n=240: resolved as power artifact (SURVIVES) or genuine non-equivalence (FALSIFIED/MIXED)
2. Threshold tautology (V3): sensitivity analysis reveals discriminating threshold range

Either outcome changes C-FRESHNESS claim ceiling and product architecture decision.

## 11. Product consequences

**If SURVIVES (all C1-C5 pass):**
- TOST lower-tail failure resolved as sample-size artifact
- Token_refresh detection confirmed robust to noise with full TOST equivalence at delta=0.15
- Parallel-channel architecture validated for token_refresh inclusion
- Moves C-FRESHNESS toward PRODUCT_CORE eligibility (pending production-substrate validation)
- Orthogonality confirmed across 4 independent mock experiments (3 prior + this one)

**If FALSIFIED:**
- Token_refresh detection fragile at n=480 or TOST equivalence impossible even at adequate power
- Parallel-channel architecture cannot include token_refresh
- C-FRESHNESS claim ceiling remains bounded to permission_boundary and session_invalidation only
- Requires alternative detection strategy or fused classifier for token_refresh

**If MIXED (C1-C4 pass, TOST fails):**
- Token_refresh detection TP and variance confirmed at n=480
- TOST equivalence not achievable at delta=0.15 even with adequate power
- Correlation may be genuinely non-zero (CI extends below -0.15)
- Requires investigation: is the non-equivalence from token_refresh behavioral-structural correlation or sample heterogeneity?
- Product decision: cautious inclusion with delta relaxation or separate handling

## 12. Inherited carry-forward

Preserved from parent handoff (EXP-PRODUCT-35456068953):

**Established:**
- Token_refresh TP=1.0 under co-occurring structural noise (4 conditions) on stochastic mock
- Stochastic token_refresh produces behavioral variance: bimodal scores 0.35/0.65, std 0.128-0.143
- Structural signal discriminates auth states: discrimination 0.8333
- Behavioral signal detects all 3 drift types with TP=1.0 in isolation
- No behavioral false positives: FP=0.0 on 240 noise-only samples
- C-FRESHNESS orthogonality at delta=0.15 confirmed across 3 prior mock experiments (n>=480)
- C-PRODUCT-ECON is REJECTED

**Rejected:**
- C-PRODUCT-ECON (token-based deduplication economics): REJECTED
- Original behavioral scoring weights: FALSIFIED
- Six structural signal families: FALSIFIED

**Unknown:**
- Whether orthogonality survives on non-mock production-like substrate (primary bottleneck for PRODUCT_CORE, gated on runtime lane)
- Whether expired/invalid fingerprint collision generalizes to production
- Whether within-condition behavioral/structural variance maintains on real network RTT

**Do not assume:**
- C-FRESHNESS is VALIDATED or PRODUCT_CORE — remains EXPERIMENTAL
- Audit REVISE implies scientific negative — frozen decision conditions all pass
- Structural signal generalizes to production OAuth/OIDC
- Token_refresh TP=1.0 generalizes to production (threshold tautology)
- Behavioral variance range reflects production severity distributions
- Four mock experiments confirm production will behave identically
