# EXP-PRODUCT-35538865048 — Report

**Lane:** product — **Claim:** C-FRESHNESS — **Status:** COMPLETE — **Outcome:** SUPPORTS (frozen SURVIVES_CURRENT_TEST)

## Question
When token_refresh behavioral scores are produced as a continuous severity gradient (not bimodal 0.35/0.65), can a calibrated discriminating threshold be found that achieves TP >=0.85 AND FP <=0.10 simultaneously — and does behavioral-structural orthogonality (TOST delta=0.15, n>=480) survive at that calibrated threshold under co-occurring production-like structural noise?

## Hypothesis
Continuous severity model mapping token_refresh outcome quality to behavioral_score in [0.2,0.8] yields a calibrated threshold in [0.40,0.60] where TP>=0.85, FP<=0.10, and orthogonality CI upper <0.15 at n=480.

## Design Summary
- **Mock server:** Flask 3.1.3 + SQLite WAL + TTLCache 0.5s + jitter 10-100ms + HS256/RS256 JWT, modified to inject continuous `session_quality` in `/api/session/status`. Token_refresh success: 50% full 0.70-0.80, 50% partial 0.50-0.69 (p=0.7 overall success); failure 0.20-0.39 (p=0.3); noise-only (no drift) 0.05-0.14. Behavioral_score = `session_quality` normalized to [0,1]. Structural noise 4 types unchanged but **FIXED** error_format_variation: body replaced BEFORE `make_response`.
- **Phase C:** 40 probes (10 per auth state) for structural discrimination.
- **Phase A:** 240 token_refresh + 240 noise-only (4 types x60) paired (behavioral+structural) for threshold calibration. Sweep [0.20,0.25,...,0.80] at 0.05 increments, compute TP/FP/F1/precision/recall, select argmax F1 subject to TP>=0.85 FP<=0.10.
- **Phase B:** 480 paired samples across 4 co-occurring token_refresh x noise (120 each) at calibrated threshold for orthogonality (Pearson r, Fisher-z CI, TOST delta=0.15).
- **Determinism:** global RNG seeded 42 before server start, `threaded=False`, sequential client, raw_evidence preserved.

## Results (Raw → Observation → Measurement → Interpretation)

### Positive Control (C1)
- **C1 discrimination:** 0.8333 >0.5 **PASS** — 3 unique fingerprints (expired/invalid collide on 401). Baseline status-only 0.5, body-only 0.8333 replicates parent.

### Threshold Calibration (Phase A)
- **Continuous injection verified:** 451 unique behavioral scores (>5 threshold) — not bimodal.
- **Sweep (13 thresholds):**
  - T=0.20 TP=1.00 FP=0.00 F1=1.00 **meets**
  - T=0.25 TP=0.9167 FP=0.00 F1=0.9565 **meets**
  - T=0.30 TP=0.85 FP=0.00 F1=0.9189 **meets**
  - T=0.35 TP=0.7833 FP=0.00 F1=0.8785 **fails TP**
  - T=0.40 TP=0.7125 FP=0.00 F1=0.8321 **fails**
  - T=0.45-0.50 plateau 0.7125, then decline to 0.00 at 0.80.
  - FP=0.00 at all thresholds — noise max 0.14 <0.20.
- **Calibrated threshold:** 0.20 (argmax F1=1.0 among 0.20/0.25/0.30; lowest wins). **Not in hypothesized [0.40,0.60]** — hypothesis interval miss but constraints met. TP at calibrated =1.0 (Wilson lower 0.9842 >=0.80), FP 0.0 <=0.10, F1 1.0.
- **Interpretation:** V-THRESHOLD-TAUTOLOGY partially resolved: unlike parent flat TP=1.0 across 0.15-0.35 and cliff to 0.677 at 0.40, continuous scores show gradual decline (1.00→0.917→0.85→0.78) beginning at 0.25, demonstrating threshold now discriminates severity. However calibrated optimum remains at low edge because noise distribution (0.05-0.14) is fully separated from failure minimum 0.20 — FP never binding, so optimum is lowest feasible threshold.

### Co-occurring Robustness at Calibrated Threshold (Phase B, n=480)
- **Per-condition behavioral_std:** pagination 0.201, variable_length 0.1971, error_format 0.1992, cdn_cache 0.1957 — all >0.05 (4/4 **PASS**).
- **TP at calibrated 0.20:** 1.0 on all 4 conditions (Wilson lower 0.969) **PASS** (requires >=0.85).
- **Structural_std:** 0.4017-0.9567; error_format_variation 0.4017 >0.15 so **not inert** — 4/4 effective coverage achieved (fix verified).
- **C2 (TP >=0.85 Wilson >=0.80): PASS** (1.0, Wilson 0.9842 token-calibration and 0.969 per co-occurring).
- **C4 (FP <=0.10): PASS** (0.0 at calibrated; per-noise FP 0.0, behavioral_mean 0.093-0.10).

### Orthogonality (C3/C5, n=480 pooled)
- **Pooled r=-0.0065, p=0.887 (ns), 95% CI [-0.0959, 0.0831], SE 0.0458.**
- **TOST at delta=0.15:** p_upper 0.000288 <0.05 **PASS**, p_lower 0.00079 <0.05 **PASS**, CI upper 0.0831 <0.15 **PASS**.
- **C3 (variance >0.05 all 4 + CI upper <0.15): PASS**
- **C5 (TOST pass): PASS**
- This is the **6th** independent mock orthogonality confirmation at delta=0.15 (prior 5: r 0.046, 0.0022, -0.0258, -0.0366, 0.016). Continuous severity extends series.

### Baselines
- **B-TAUT-025:** Expected tautological 1.0 at 0.25; observed 0.9167 at 0.25 now discriminates (decline from 1.0 at 0.20) — tautology reduced.
- **B-MODE-MID-050:** Expected ~0.70 at 0.50; observed 0.7125 at 0.50 matches but plateau from 0.40 indicates failure cluster below 0.40 and success cluster above.
- **B-PARENT-N480-MOCK:** Parent TOST PASS with r=0.016 CI Upper 0.1055; current r=-0.0065 CI Upper 0.0831 also **PASS** — continuous extension.
- **B-5X-ORTHO-MOCK:** 6th PASS confirms series.

### Decision Rule
**SURVIVES_CURRENT_TEST requires ALL:**
- C1 0.8333>0.5 ✓
- C2 TP 1.0>=0.85 Wilson 0.9842>=0.80 ✓
- C3 behavioral_std >0.05 (4/4) and CI Upper 0.0831<0.15 ✓
- C4 FP 0.0<=0.10 ✓
- C5 TOST PASS ✓
→ **SURVIVES_CURRENT_TEST → canonical SUPPORTS.**

**MEASUREMENT_INVALID triggers checked:** continuous 451>=5 ✓, error_format not inert ✓, n=480 ✓. Not invalid.

**FALSIFIED trigger:** No threshold fails — calibrated exists, so not falsified.

## Validity & Limitations
- **Mock-only ceiling** still applies (localhost, no real OAuth/OIDC/CDN/RTT/DB).
- **Hand-designed severity:** mapping is synthetic; production refresh quality distribution unknown.
- **Noise separation gap:** noise-only 0.05-0.14 vs failure min 0.20 creates perfect separation by design; production may have overlapping distributions, making FP binding. Threshold at 0.20 is low-edge optimum, not middle-range as hypothesized.
- **FP never binding** (0.0 at all thresholds) means FP constraint not tested discriminatingly — inference limited to this separation.
- **Hypothesis interval miss:** predicted [0.40,0.60] not achieved; evidence supports existence of calibrated threshold but not at predicted location. Threshold tautology moved from 0.25 bimodal to 0.20 low edge, not to mid-range.

## Product Consequence
- **Positive (this outcome):** Threshold tautology partially resolved — continuous severity introduces discriminating TP decline. Calibrated operating point exists with perfect F1 at low threshold, orthogonality survives at delta=0.15. Moves C-FRESHNESS toward VALIDATED **but bounded to mock substrate**; production gate remains open. Supports claiming freshness guard can discriminate continuous severity at non-tautological (though still low) threshold.
- **If negative (not observed):** Would have shown no threshold achieves both constraints or orthogonality breaks, downgrading C-FRESHNESS as viability limited to bimodal tautological detection without fundamentally different signal.

## Economics
- ~1000 HTTP cycles (40 probes + 480 Phase A + 480 Phase B paired with 960 GETs), runtime ~116s single-threaded, no LLM cost, negligible compute. Reuses parent harness with minimal code change (session_quality injection + error_format fix).

## Evidence References
- `raw_evidence/experiment_data.json` sha256 e11daecdc919180373d3ad928ef9920b3ae3e7913c8def779c16b529003ab2a0
- `mock_server.py` sha256 c90fc51d0c670ba81574275bce3b1eae51a6b7639714504817013c58ebbbbea4
- `run_experiment.py` sha256 644f72ce2de3363a53e8bd1982e7f3eb7d529d8a27bad181ce64cd82ce48f0dc
- `result.json` sha256 4043bff6c382d63a2a9f9969e8beea07e0cbeaab10c81e99a85ecaf6a7ae600d
- Parent handoff `EXP-PRODUCT-35481773764/handoff.json` sha256 b3e8f204...

## Unresolved
- Production threshold calibration requires overlapping noise/refresh distributions.
- Production substrate orthogonality still untested.
- Partial vs full success mixture sensitivity.

---
*Generated from raw_evidence → observations → metrics → interpretation; frozen inputs immutable.*
