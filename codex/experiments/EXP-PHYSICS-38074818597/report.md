# EXP-PHYSICS-38074818597 — EXECUTE report

- Lane: **physics**; target claim **C-WEB-DYNAMICS** (no promotion).
- Frozen branch: **S1_STATIONARY**; measurement valid: **True**.
- Anchor T0 histogram: `{'CLEAN': 45, 'OTHER_NONBARRIER': 4, 'BLOCK_403_CHALLENGE': 6, 'RATE_LIMIT_429': 1, 'TRANSPORT_ERROR': 1}`
- delta_ref histogram: `{'CLEAN': 46, 'BLOCK_403_CHALLENGE': 6, 'OTHER_NONBARRIER': 4, 'TRANSPORT_ERROR': 1}`
- n_t0_intrinsic=7, n_t0_barrier=8, f_b_obs=0.140351
- delta_ref actual = 1800 s; rung actual deltas = {'0': 1.1920928955078125e-06, '1': 300.00021171569824, '2': 900.0002288818359, '3': 1800.0002045631409}

## Primary quantities

- STATIONARITY_SKILL = **0.319601 nats**; B_EXCHANGE p = 9.999e-05; clustered CI95 = ['0.142431', '0.495411']
- STATIONARITY_SKILL_BY_RUNG = {300: 0.4056, 900: 0.4056, 1800: 0.319601}
- STATIONARITY_SKILL_NO_STRESS = 0.395067 (p=9.999e-05)
- MI_CLASS = 0.66738
- CLASS_PERSISTENCE = {'CLEAN': 1.0, 'RATE_LIMIT_429': 0.0, 'BLOCK_403_CHALLENGE': 1.0, 'TRANSPORT_ERROR': 1.0, 'OTHER_NONBARRIER': 1.0}
- INTRINSIC_PERSISTENT = **True** (pooled persistence 1, present classes ['BLOCK_403_CHALLENGE', 'TRANSPORT_ERROR'])
- DENYLIST_FALSE_ACCEPT = 0, DENYLIST_FALSE_REJECT = 0, DENYLIST_INTRINSIC_VALID = **True**
- DENYLIST_HORIZON = 1800 s; DENYLIST_BY_RUNG = {300: {'valid': True, 'false_accept': 0.0, 'false_reject': 0.0}, 900: {'valid': True, 'false_accept': 0.0, 'false_reject': 0.0}, 1800: {'valid': True, 'false_accept': 0.0, 'false_reject': 0.0}}
- ANYBARRIER_FALSE_ACCEPT = 0.125; DENYLIST_SKILL = 1.69664 nats
- rate diagnostics: RATE_ONSET_n=0, RATE_RECOVERY_n=1, RATE_RECOVERY_HALF_LIFE_s=2, AMBIENT_RATE_ONSET_n=0, AMBIENT_RATE_RECOVERY_n=1, CLASS_CONDITIONAL_TRANSIENCE=True
- self-induction: no-stress barrier prevalence by rung = {0: 0.1346, 300: 0.1346, 900: 0.1346, 1800: 0.1346}, slope=0/s, CI=['0', '0']

## Controls and baselines

- **PC_SYNTHETIC_STATIONARY**: pass=True; expected: S1 selection fraction >= 0.80 at rho=0.98
- **NC_SYNTHETIC_EXCHANGEABLE**: pass=True; expected: B_EXCHANGE p<0.05 fraction <= 0.05
- **PC_ORACLE_BARRIER**: pass=True; expected: every oracle request classified into its expected class
- **NC_CLEAN_ORACLE**: pass=True; expected: all requests classify CLEAN
- **C_PROBE_SELF_INDUCTION**: pass=None; expected: no hard pass/fail; report self-induction trend
- **B_EXCHANGE**: pass=None; expected: primary strong null: anchor barrier indicator carries no info beyond marginal
- **B_CONSTANT_USABLE**: pass=None; expected: no-denylist floor (predict non-barrier)
- **B_MARGINAL**: pass=None; expected: constant-marginal diagnostic
- **B_LASTSWEEP**: pass=None; expected: recent-memory diagnostic

## Branch decision (frozen rule)

decision_rule: MEASUREMENT_INVALID first, then S1 if (INTRINSIC_PERSISTENT AND DENYLIST_INTRINSIC_VALID AND STAT_SIG), else S0.
change evidence classes: []

## Interpretation (bounded)

On this frozen pool/window and one egress vantage the intrinsic access-barrier state is consistent with stationarity at the tested timescales: intrinsic classes persisted, the intrinsic denylist remained valid through the tested horizon, and the anchor barrier indicator carried information beyond the exchangeable constant null. Product reading (bounded): a static intrinsic denylist built at one window remained valid through the measured horizon (>=1800 s, right-censored).

## Validity notes

- Single network vantage / single stdlib client / single ~2041s session; the source-vantage axis is a declared scope boundary (spec.scope_boundaries).
- The denylist horizon is right-censored at delta_ref=1800 s; no information beyond the tested ladder is claimed.
- DENYLIST_FALSE_REJECT uses the frozen falsifier/prereg denominator |T0 non-intrinsic| (design_review N3 resolved in favour of falsifier/prereg over the conflicting decision_rule wording).
- DENYLIST_SKILL is reported on the intrinsic indicator (anchor intrinsic-transfer predictor vs constant non-intrinsic); the frozen name does not specify the smoothing, so clipping eps=1e-6 is used and the operational definition is recorded in metrics.
- PC_SYNTHETIC_STATIONARY uses the control's own literal perms_per_rep=500 and R=300 with a 500-resample clustered bootstrap for the CI clause (design_review N4 notes the 10000-permutation inconsistency in thresholds_frozen); the pass gate is the rho=0.98 S1 fraction.
- The induced-transience probe interleaves the 5 stress endpoints' recovery ladders at each nominal delay after each endpoint's own burst rather than serializing whole endpoints; Q3 is a reported refinement that never gates S1/S0.
- Body SHA-256 and the stored classifier prefix are the first 262144 bytes (the frozen match scope); a printable 8192-char prefix is stored for auditability.
- The pre-freeze census/calibration /tmp artifacts cited in spec/prereg are absent and are declared non-interpretation-dependencies (design_review N1/N2); EXECUTE re-derived all floors, controls and metrics from its own raw data.
- The pre-freeze census is outcome-adjacent pilot evidence on parent-inherited endpoints, not the frozen 4-sweep/1800 s measurement; it does not certify persistence at 1800 s (prereg validity threat 10).

## Unresolved

- Does endpoint access-barrier persistence generalize beyond this frozen 57-endpoint pool, this single egress vantage and this ~30-minute window? The source-vantage axis is untested.
- Is the measured horizon censored: would the intrinsic denylist remain valid at delta > 1800 s?
- ONSET (CLEAN->intrinsic) at higher request rates or longer sequences remains untested outside the fixed 8-GET stress burst.
- The simultaneous role of protocol self-induction cannot be fully removed; C_PROBE_SELF_INDUCTION only bounds ambient barrier prevalence on the 52 non-stress endpoints.

## Provenance

Run id `38117210627`; raw evidence under `raw/`; code hashes in `provenance.json`; classifier replay mismatches = 0.

