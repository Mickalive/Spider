# Preregistration: EXP-PHYSICS-35389142077

## Background

The parent experiment (EXP-PHYSICS-35375596894) achieved a major milestone: state-history K=2 conditional PMI = 0.933 bits (p=0.001, d=25.9) on the 12-state SPA simulation at N=5000, confirming the beyond-Markov signal is real and detectable. The parent also showed action-history K=3 at N=5000 = 1.221 bits, demonstrating the parent's N=1000 failure was primarily sparsity, not conditioning strategy.

However, the frozen decision rule evaluated MEASUREMENT_INVALID due to null control failure (C4): trajectory-level block permutation yielded null_mean=0.552 at K=2 (31x the 3*std threshold). The audit confirmed this bias is intrinsic to hash-routed SPA design — block permutation shuffles (url_before, url_after) pairs while keeping history fixed, but history was computed from original url_before sequence, creating artificial state-history correlations.

The parent handoff identified the corrective action: replace trajectory-level block permutation with within-stratum conditional permutation (shuffle url_after within each (url_before, H_K) stratum). This preserves marginal transition probabilities within each stratum while breaking the action-PMI coupling, and should center the null at zero because the artificial state-history correlation is eliminated.

The parent also identified that production SPA testing is the critical next step after methodology validation. Previous production attempts (EXP-PHYSICS-35308806126) failed due to anti-bot blocking (0 NL transitions on BBC News, Amazon, Twitter/X).

### Parent carry_forward

- **Established:**
  - URL-level PMI (fragment-preserving) reproduces parent signal: unconditional K=0 PMI = 1.419 bits (p=0.001, d=321). K=1 state-history PMI = 1.531 bits (p=0.001, d=80.7). (result.json:metrics.unconditional_pmi_k0, state_history_pmi_k1)
  - PMI pipeline correctly detects beyond-Markov structure when present: positive control (8-state deterministic SPA N=5000) achieves state K3 PMI = 1.671 bits (p=0.001, d=87.9), action K3 = 1.806 bits (p=0.001, d=103.2). (result.json:controls.POSITIVE_CONTROL_SYNTHETIC_SPA)
  - 12-state SPA simulation has beyond-Markov structure BY CONSTRUCTION: at K=2 state-history, 885/1292 strata (68.5%) are stochastic; at K=3, 978/2779 (35.2%) stochastic. (result.json:metrics.determinism_check_state_k2, determinism_check_state_k3)
  - State-history K=2 conditional PMI = 0.933 bits (p=0.001, d=25.9) at N=5000 on 12-state SPA. 398/1292 strata used (30.8%). Parent sparsity bottleneck resolved. (result.json:metrics.state_history_pmi_k2)
  - Action-history K=3 at N=5000 = 1.221 bits (p=0.001, d=14.2), 510/821 strata used (62.1%). Parent failure was primarily sparsity (N=1000), not conditioning strategy. (result.json:metrics.action_history_pmi_k3)
  - Fragment-stripping normalization destroys all state information. (parent carry_forward.established)
- **Rejected:**
  - Beyond-Markov URL-level PMI on TodoMVC hash-SPAs: 0/5 variants achieve K3 PMI > 0.05 bits. (EXP-PHYSICS-35290611436, EXP-PHYSICS-35308806126)
  - Title-aware PMI on TodoMVC: 0/5 variants have >=2 unique titles. (EXP-PHYSICS-34266105229, EXP-PHYSICS-35209110569)
  - State-history conditioning is NECESSARY for beyond-Markov detection: action-history K3 at N=5000 (1.221 bits) outperforms state-history K2 (0.933 bits). (this experiment's parent)
- **Unknown:**
  - Whether within-stratum conditional permutation centers null at 0 for hash-routed SPAs. This is the prerequisite methodology fix for C4 compliance.
  - Whether Playwright browser automation yields identical transition distribution to in-memory simulation.
  - Whether URL-level PMI with N>=5000 detects beyond-Markov dynamics on production SPAs.
  - Whether richer state representations (DOM hash, accessibility tree, visual layout) yield marginal information beyond URL+state-history.
  - Optimal history length K for detection given state/action cardinalities.
- **Do not assume:**
  - C-WEB-DYNAMICS is globally false. The experiment confirms beyond-Markov structure exists and is detectable (K2 PMI 0.933 bits, p=0.001). The MEASUREMENT_INVALID verdict is due to null control methodology limitation, not absence of signal.
  - The null control failure (C4) is evidence against beyond-Markov signal. The permutation bias is intrinsic to hash-routed SPA design; the p-value (0.001) remains a valid significance test.
  - State-history conditioning is necessary. Action-history K3 at N=5000 (1.221 bits) outperforms state-history K2 (0.933 bits).
  - The PMI pipeline is broken. Positive control validates it.
  - Results generalize to production SPAs. The 12-state simulation has 12 states, 4 deterministic candidates, hash-based selection, and no anti-bot, auth, or visual complexity.
  - The provenance artifact hashes are correct. Audit found SHA256 mismatches for raw_transitions.json and analysis_results.json.

## Hypothesis

**H1 (null centering — primary):** Within-stratum conditional permutation (shuffle url_after within each (url_before, H_K) stratum, 1000 perms) yields null mean PMI within [-0.1, +0.1] bits of zero at K=2 on the 12-state SPA simulation with N=5000. This resolves the inherited C4 failure (parent null_mean=0.552).

**H0 (null not centered):** |within_stratum_null_mean_K2| >= 0.1 bits, indicating the revised permutation does not eliminate the bias.

**H2 (production detection — conditional on H1):** At least 1 of 3 candidate production SPAs achieves conditional PMI > 0.05 bits at K=2 with N>=5000 non-leakage transitions and valid null (|null_mean| < 0.1).

**H0_production:** All production SPAs achieve K2 PMI <= 0.05 bits OR fail to collect >=5000 NL transitions.

**Rationale for within-stratum conditional permutation:** The parent's block permutation bias arose because shuffling (url_before, url_after) pairs while keeping history fixed created artificial state-history correlations (history was computed from original url_before sequence). Within-stratum permutation eliminates this by: (1) fixing the stratum key (url_before, history), so history is held constant; (2) shuffling only url_after within each stratum, preserving P(url_after|stratum) while breaking I(url_after; action|stratum). Under this null, action and url_after are independent within each stratum, so E[PMI_null] = 0 analytically. Deterministic strata (single url_after) contribute PMI=0 regardless, same as parent.

## Methods

### Phase 1: Simulation Null Centering (required before Phase 2)

#### Testbed

Same 12-state SPA simulation as parent (EXP-PHYSICS-35375596894):
- 12 unique URL states with hash-based routing
- 4 action primitives: form_submit, button_click, js_navigate, menu_select
- Stochastic transitions: choose_next(prev1, prev2, current, action) selects from 4 candidates via SHA256(prev1:prev2:current:action) mod 4
- In-memory simulation

#### Data Collection

- N=5000 transitions: 50 sessions x 100 steps, seed=42 (same as parent)
- State-history H_K built from URL states with START_TOKEN padding

#### Within-Stratum Conditional Permutation

For each permutation:
1. Group records by (url_before, history) stratum
2. Within each stratum with >= MIN_STRATUM_SIZE records, shuffle url_after values randomly
3. Keep (url_before, history, action) fixed within each stratum
4. Recompute conditional PMI on shuffled records
5. Repeat 1000 times, seed=42

This preserves P(url_after | stratum) while making action and url_after independent within each stratum. Expected null mean = 0 bits.

#### Comparison Baselines (Phase 1)

- Trajectory-level block permutation (parent method, expected biased)
- Within-stratum conditional permutation (new method, expected centered)
- Action-shuffle diagnostic (parent method, expected biased)

### Phase 2: Production SPA Testing (conditional on Phase 1 null centering)

#### Production SPA Candidates

Three locally-hosted or production-friendly SPAs with hash-based or history-based routing:
1. **TodoMVC SPA variants** (already validated, but constant titles — test URL-level PMI only)
2. **Custom production-like SPA** with state-dependent content, auth state, and >= 10 states
3. **External production SPA** (if automatable without anti-bot blocking)

For each site:
- Use Playwright browser automation (Chromium) to collect transitions
- Action discovery: random exploration with form_submit, button_click, js_navigate, menu_select
- Non-leakage filter: exclude transitions where action.target_href == state_after.url
- Target: >= 5000 non-leakage transitions per site
- Record DOM hash, accessibility tree hash alongside URL for future representation experiments

#### Analysis

- Same PMI pipeline as Phase 1 (alpha=0, MIN_STRATUM_SIZE=5, weighted average)
- Within-stratum conditional permutation null (validated in Phase 1)
- K=2 state-history conditioning
- Bonferroni correction for 3 confirmatory tests: alpha = 0.0167

## Decision Rule

**Phase 1 (simulation null centering):**
- SURVIVES if ALL: (a) |within_stratum_null_mean_K2| < 0.1 bits; (b) positive control passes (K3 PMI >= 1.0 bits, p < 0.001); (c) K2 PMI > 0.05 bits
- FALSIFIED-IN-SETTING if |within_stratum_null_mean_K2| >= 0.1 bits (methodology does not center null)
- MEASUREMENT_INVALID if controls fail or data quality insufficient

**Phase 2 (production detection, only if Phase 1 SURVIVES):**
- SURVIVES_CURRENT_TEST if >= 1/3 production SPAs achieves K2 PMI > 0.05 bits with |null_mean| < 0.1 AND N >= 5000 NL
- FALSIFIED-IN-SETTING if 0/3 production SPAs achieve K2 PMI > 0.05 bits (with valid null and sufficient N)
- MEASUREMENT_INVALID if 0/3 sites achieve >= 5000 NL transitions (infrastructure failure)

## Validity Threats

1. **Within-stratum permutation may not center null at zero.** The analytic argument is sound (preserves P(url_after|stratum) while breaking action coupling), but the specific stratum structure of hash-routed SPAs could introduce finite-sample bias. Mitigation: compare against block permutation (known biased) and action-shuffle as diagnostics.

2. **Deterministic strata dilution.** At K=2, ~31.5% of strata are deterministic (single url_after), contributing PMI=0 regardless of permutation. This dilutes the weighted average but does not bias the null — deterministic strata contribute 0 to both observed and null PMI. The null mean should still center at 0.

3. **Small strata at K=3.** State-history K=3 has 2779 total strata but only 105 used (3.8%) at N=5000. K=2 (1728 strata, 30.8% used) is the appropriate primary test. K=3 is exploratory.

4. **Production SPA anti-bot blocking.** Previous attempts (EXP-PHYSICS-35308806126) yielded 0 NL transitions on BBC News, Amazon, Twitter/X. Mitigation: use locally-hosted SPAs with known routing as primary candidates; external production SPAs are exploratory.

5. **Playwright chromium availability.** CI may not have Chromium installed. Mitigation: if Chromium unavailable, Phase 2 falls back to HTTP API collection (same as parent automatability diagnostic), limiting browser-specific validation.

6. **Non-leakage filter stringency.** The action.target_href == state_after.url definition may be too strict for production SPAs where URL routing is not fragment-based. Mitigation: report both raw and NL-filtered transition counts; if NL < 5000, report raw count and explain filter impact.

## Expected Outcomes and Consequences

**If Phase 1 SURVIVES (null centered, signal detected):**
- The PMI pipeline becomes measurement-valid for hash-routed SPAs
- The inherited MEASUREMENT_INVALID verdict is resolved
- C-WEB-DYNAMICS advances from HYPOTHESIS toward EXPERIMENTAL (pending Phase 2)
- Subsequent Physics experiments can use within-stratum permutation as the standard null control

**If Phase 1 FALSIFIED (null not centered):**
- Within-stratum conditional permutation does not resolve the bias
- The null control problem requires fundamental rethink (model-based null, parametric bootstrap, or alternative falsification framework)
- The 0.933-bit K2 PMI remains an observation but cannot support a confirmatory claim
- The Physics lane should consider alternative detection methods (e.g., conditional entropy, transfer entropy, or model-based approaches)

**If Phase 1 SURVIVES but Phase 2 FALSIFIED (production SPA signal absent):**
- URL-level PMI is insufficient for production SPAs beyond synthetic testbeds
- Richer state representations (DOM, accessibility tree, visual) or different detection methods needed
- C-WEB-DYNAMICS claim ceiling bounded to synthetic SPAs

**If both phases SURVIVE:**
- C-WEB-DYNAMICS supported on production SPAs with URL-level representation
- Major breakthrough for Web Physics: genuine beyond-Markov dynamics detected on real Web
- Product consequence: mechanical priors for exploration become empirically grounded
