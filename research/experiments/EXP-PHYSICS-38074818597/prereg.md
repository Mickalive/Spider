# EXP-PHYSICS-38074818597 — Preregistration (frozen before execution)

Lane: **physics**. Target claim: **C-WEB-DYNAMICS**. Director mandate action: **REOPEN**, cognitive reset, `parent_handoff_disposition` **USE**. `design_contract_version = 2`.

`spec.json` is the machine-binding source; where wording differs, `spec.json` governs. Do not edit after `freeze.json` exists.

## 1. What is tested

On the frozen 57-endpoint credential-free HTTP GET universe (inherited verbatim from `EXP-PHYSICS-37992957068`; **not extended**, because the pre-freeze attainability certificate in §6 is satisfied inside the frozen 57) we measure the **persistence/timescale of each endpoint's INTRINSIC ACCESS-BARRIER state** across a ladder of separated ambient observation windows, and the **validity horizon of a static endpoint-level denylist** built on those intrinsic classes.

Concretely:

- **Q1 (stationarity).** Across a window ladder anchored at T0 with nominal revisits at +300 s, +900 s and +1800 s, do the intrinsic classes `{BLOCK_403_CHALLENGE, TRANSPORT_ERROR}` persist at an endpoint (`CLASS_PERSISTENCE` per present intrinsic class `>= 0.80`), and is the anchor-to-lag barrier-state identity transfer `I(B_0; B_delta)` distinguishable from an exchangeable / constant-memory null?
- **Q2 (denylist validity horizon)**: does a static endpoint-level denylist built over the intrinsic (persistent) barrier classes at T retain validity at `T+delta` (`FALSE_ACCEPT` = a denylisted intrinsic endpoint is non-intrinsic at `T+delta`; `FALSE_REJECT` = a non-intrinsic endpoint becomes intrinsic), and what is its measured horizon?
- **Q3 (class-conditional, reported refinement)**: is the rate-driven class `RATE_LIMIT_429` transient (induced recovery/onset within seconds-to-minutes) while the intrinsic classes persist, so that the product needs a class-conditional policy rather than one pooled denylist?

This changes the unit of study from *next-request* barrier classification (bounded by `EXP-PHYSICS-37992957068`) to *endpoint access-state persistence across separated windows*. It is orthogonal to the exhausted next-request / value-derivation / PMI sub-threads, to Graph `C-FRESHNESS` (staleness of inherited *content*) and to Runtime drift controls. The temporal/window axis is measured; the mandate's **source-vantage** axis is **not** varied and is a declared scope boundary (one stdlib-HTTP egress, one continuous ~45-minute session).

### 1.1 Branch design (two-sided, both directions reachable)

- **S1_STATIONARY**: `INTRINSIC_PERSISTENT` AND `DENYLIST_INTRINSIC_VALID` AND `STAT_SIG`.
- **S0_NON_STATIONARY**: the measurement is valid AND NOT `S1_STATIONARY`. Its frozen positive-evidence classes are (a) `INTRINSIC_PERSISTENT` false (a durable intrinsic barrier changed class), (b) `DENYLIST_INTRINSIC_VALID` false (a denylisted endpoint recovered, or a clean endpoint newly and durably blocked), (c) `STAT_SIG` false (anchor→lag barrier information is no better than the exchangeable constant null).
- **MEASUREMENT_INVALID**: reserved **exclusively** for prerequisite/control failure; MUST NOT be reported as a scientific `S0_NON_STATIONARY`.
- `CLASS_CONDITIONAL_TRANSIENCE` (Q3) is a **reported refinement** of whichever primary disposition holds; it is never a pre-empting branch. The prior-draft trap (making the support branch require the absence of protocol-induced rate transients) is deliberately removed: `RATE_*` and `AMBIENT_RATE_*` never gate a primary branch.

## 2. Frozen intrinsic classifier (response-intrinsic, no history leakage)

Each response is classified from its own stored fields only (status, `cf-mitigated`, first 262144 body bytes, transport error string). The frozen challenge-marker regex is transcribed verbatim:

```
CHALLENGE_RE_LITERAL = (?i)(just a moment|cf-browser-verification|cf[-_]chl[-_]|challenge-platform|cf-challenge|cdn-cgi/challenge|attention required|checking your browser|enable javascript and cookies|verify you are human|please complete the security check|g-recaptcha|hcaptcha|recaptcha|cf-turnstile|<title>\s*just a moment)
```

| class | rule |
|---|---|
| `CLEAN` | status in 200..299 (2xx) and body does not match `CHALLENGE_RE` |
| `RATE_LIMIT_429` | status == 429 |
| `BLOCK_403_CHALLENGE` | status == 403 and (`cf-mitigated: challenge` **or** body matches `CHALLENGE_RE`) |
| `UNAVAILABLE_403` | status == 403 without any challenge marker |
| `TRANSPORT_ERROR` | no HTTP response (DNS/connect/TLS/timeout) |
| `OTHER_NONBARRIER` | any other HTTP status (404, 500, redirect chains to error) **or** a 2xx carrying a challenge marker |

`barrier_set = {RATE_LIMIT_429, BLOCK_403_CHALLENGE, TRANSPORT_ERROR}`. `ordinary_unavailability_set = {UNAVAILABLE_403, OTHER_NONBARRIER}`. `intrinsic_classes = {BLOCK_403_CHALLENGE, TRANSPORT_ERROR}`. `severity_rank`: `TRANSPORT_ERROR 5 > RATE_LIMIT_429 4 > BLOCK_403_CHALLENGE 3 > UNAVAILABLE_403 2 > OTHER_NONBARRIER 1 > CLEAN 0`. All classes are functions of a single request's stored fields only, so conditioning on the anchor state is not label leakage.

## 3. Frozen sweep protocol and strata

**Unit**: `(endpoint, sweep_index)`; anchor = sweep 0 (T0).

**Ladder** (nominal offsets, seconds): `[0, 300, 900, 1800]`; `ladder_s = [300, 900, 1800]`; `delta_ref = 1800`. Analysis labels each sweep by its **nominal rung**; the `delta_ref` sweep's **actual** delta must be ≥ 1500 s or the run is `MEASUREMENT_INVALID`.

**Request policy**: GET only, follow ≤ 5 redirects, 30 s timeout, TLS verification on, **no retries, one attempt per observation** (so a DNS/connect/TLS/timeout failure is directly `TRANSPORT_ERROR`, not a retried `CLEAN`). Frozen User-Agent `SPIDER-research2/1.0 (+credential-free access-state persistence probe)`, `Accept: */*`. No authentication, JavaScript or credentials. Python 3.12 **stdlib only** (numpy is not required or imported).

**Ambient probe (primary state)** — for EVERY endpoint: a fresh cookie jar, then exactly **one** GET. `ambient_class` = classifier output. Endpoints are probed sequentially in a per-sweep frozen seeded permutation (seed `38074818597`), inter-endpoint gap 0.30 s. **The primary state for all stationarity/denylist metrics is `ambient_class`.**

**Induced-transience probe (Q3, diagnostic only)** — executed ONCE, AFTER the 1800 s rung, on `stratum_stress` only: a fresh cookie jar, then a burst of `B_stress = 8` GETs at gap 0.15 s; `load_class` = max severity rank over the 8. Then single cold probes (fresh jar) at nominal delays 2, 5, 15, 60, 180 s after the burst, recording the recovery series. The other 52 endpoints get no load probe.

**`stratum_stress`** (fixed, NOT outcome-selected): `https://www.djangoproject.com/admin/login/`, `https://www.djangoproject.com/accounts/login/`, `https://auth0.com/`, `https://search.brave.com/search?q=test`, `https://community.home-assistant.io/`.
**`stratum_intrinsic_candidates`** (fixed, reported diagnostic subgroup): `https://gitlab.com/users/sign_in`, `https://community.cloudflare.com/`, `https://www.npmjs.com/login`, `https://wordpress.com/log-in`, `https://www.phpbb.com/community/`, `https://community.invisioncommunity.com/`.

## 4. Metrics, baselines and stable identifiers

- `STATIONARITY_SKILL` (**primary**) = plug-in binary mutual information `I(B_T0; B_delta_ref)` in nats over the barrier indicator (`B = 1` iff `ambient_class ∈ barrier_set`); `B_EXCHANGE` global endpoint-permutation p-value (10000 uniform shuffles of the lag indicator across all 57 endpoints preserving both marginals; seed 38074818597); endpoint-clustered bootstrap 95% CI (cluster = `registrable_domain`; 10000 resamples; seed 38074818597).
- `CLASS_PERSISTENCE[c]` = fraction of endpoints whose T0 ambient class is intrinsic class `c` and whose `delta_ref` ambient class is also `c`. `INTRINSIC_PERSISTENT` = `(n_t0_intrinsic >= 3)` AND every intrinsic class present at T0 has `CLASS_PERSISTENCE ≥ 0.80`. `INTRINSIC_PERSISTENCE` = pooled fraction of T0 intrinsic endpoints whose `delta_ref` class equals their T0 class.
- `DENYLIST_FALSE_ACCEPT` = |{T0 intrinsic, non-intrinsic at delta_ref}| / `|T0 intrinsic|`; `DENYLIST_FALSE_REJECT` = |{T0 non-intrinsic, intrinsic at delta_ref}| / `|T0 non-intrinsic|`. `DENYLIST_INTRINSIC_VALID = (FALSE_ACCEPT ≤ 0.20) AND (FALSE_REJECT <= 0.20)`.
- `STAT_SIG = (STATIONARITY_SKILL >= 0.05) AND (B_EXCHANGE permutation p < 0.05) AND (clustered bootstrap CI lower > 0)`.
- `DENYLIST_HORIZON` = largest contiguous prefix of rungs over which `DENYLIST_INTRINSIC_VALID` holds (0 if invalid at the first rung; censored at 1800 s); `DENYLIST_SKILL` = log-loss improvement (nats/endpoint) of the anchor intrinsic-transfer predictor over `B_CONSTANT_USABLE` at `delta_ref`.
- Class-conditional diagnostics (reported refinements, non-gating): `RATE_RECOVERY_n`, `RATE_ONSET_n`, `RATE_RECOVERY_HALF_LIFE` (median first non-429 recovery-probe delay, right-censored at 180 s), `AMBIENT_RATE_ONSET_n`, `AMBIENT_RATE_RECOVERY_n`, `CLASS_CONDITIONAL_TRANSIENCE = (RATE_RECOVERY_n>0) OR (RATE_ONSET_n>0) OR (AMBIENT_RATE_ONSET_n>0) OR (AMBIENT_RATE_RECOVERY_n>0)`, `ANYBARRIER_FALSE_ACCEPT` (naive pooled-denylist cost).
- Robustness replica: `STATIONARITY_SKILL_NO_STRESS` (restricted to the 52 non-stress endpoints) and `STATIONARITY_SKILL_NO_STRESS_TREND`.

Baselines: `B_EXCHANGE` (primary strong null), `B_CONSTANT_USABLE` (no-denylist floor), `B_MARGINAL`, `B_LASTSWEEP` (diagnostics). Stable identifiers: primary metric `STATIONARITY_SKILL`; controls `PC_SYNTHETIC_STATIONARY`, `PC_ORACLE_BARRIER`, `NC_SYNTHETIC_EXCHANGEABLE`, `NC_CLEAN_ORACLE`, `C_PROBE_SELF_INDUCTION`; policies `POLICY_STATIC_DENYLIST_INTRINSIC`, `POLICY_CLASS_CONDITIONAL_DENYLIST`; branches `S1_STATIONARY`, `S0_NON_STATIONARY`, `MEASUREMENT_INVALID`. Seeds: probe_order/bootstrap/permutation/pc_synthetic = 38074818597; nc_synthetic = 38074818598.

## 5. Decision rule and thresholds

Frozen thresholds: `delta_ref_s = 1800`; `intrinsic_persistence_min = 0.80`; `tau_FA = tau_FR = 0.20`; `alpha = 0.05`; `delta_SKILL_nats = 0.05`; `pc_power_min = 0.80`; `nc_false_positive_max = 0.05`; `min_t0_intrinsic = 3`; `min_t0_barrier = 3`; 10000 permutations/resamples. Branch precedence (frozen in `spec.json.decision_rule`):

1. `MEASUREMENT_INVALID` (prerequisite/control failure only).
2. `S1_STATIONARY` if `INTRINSIC_PERSISTENT AND DENYLIST_INTRINSIC_VALID AND STAT_SIG`.
3. `S0_NON_STATIONARY` otherwise (reporting which positive-evidence class fired).

Claim ceiling: C-WEB-DYNAMICS remains **HYPOTHESIS**; `H0`/`S0` and `H2`/class-conditional bound (do not reject) a pooled static-denylist prior on this frozen pool, one vantage and one window. No PRODUCT_CORE promotion and no EXPERIMENTAL upgrade from this single window ladder.

## 6. Null calibration (pre-freeze, non-outcome-bearing)

The mandated memory/constant null is `B_EXCHANGE` (global uniform shuffle of the lag barrier indicator, both marginals preserved, recomputing `I(B_T0; B_delta_ref)`). Fresh calibration ran the **actual** estimator and the **exact** frozen branch rule on synthetic worlds — including its clustered-bootstrap CI-lower clause and the intrinsic-set-only denylist definition (no Web outcomes; script `/tmp/opencode/phys380/calibrate4.py` sha256 `3e603e32f0b62e8790fb9927c040175236e44ecff0e0d145e65786ef46426cac`, raw output `/tmp/opencode/phys380/cal4.json` sha256 `5fd08d9930ab1f1c1b5fe54a36c3fd86286bb1b9327ddef198363dfd11c2bed7`; PERM=500 and BOOT=1000 per replication, a documented approximation of the frozen 10000):

| synthetic world | MI mean (nats) | perm-sig rate | `STAT_SIG` rate | branch selected |
|---|---|---|---|---|
| `PC98` (planted-stationary, rho=0.98) | 0.3261 | 1.00 | 1.00 | `S1` 295/300 |
| `PC92` (planted-stationary, rho=0.92) | 0.2821 | 1.00 | 1.00 | `S1` 263/300 |
| `NC_EXCHANGE` (independent anchor/lag) | 0.0096 | 0.0267 | 0.0067 | `S0` 300/300 |
| `INTRINSIC_BREAK` (durable intrinsic change) | 0.0123 | 0.0300 | 0.0000 | `S0` 300/300 |
| `RATE_ONSET` (persistent intrinsic + 2 ambient rate onsets) | 0.2576 | 1.00 | 1.00 | `S1` 300/300 |

**Frozen consequence (both directions reachable):** under the exact rule, `S1_STATIONARY` is selected in 295/300 (~0.98) replications at rho=0.98 and 263/300 (~0.88) at rho=0.92 — above the `pc_power_min = 0.80` requirement; `S0_NON_STATIONARY` is selected in 300/300 intrinsic-break and 300/300 exchangeable replications. `NC_SYNTHETIC_EXCHANGEABLE` full-`STAT_SIG` false-positive = 2/300 = 0.0067 (`<= 0.05`). The `RATE_ONSET` row confirms the removed trap: ambient rate-limit onsets do **not** block `S1` because the frozen denylist is computed over the intrinsic set only, so rate transients are correctly a reported refinement rather than a gate. This calibrates the estimator, null and rule; it does not assert any real endpoint is stationary.

## 7. Attainability certificate (pre-freeze, non-outcome-bearing)

All pre-freeze activity is non-confirmatory and establishes reachability + calibration only. Scripts are under `/tmp/opencode/phys380/` and are **not** frozen interpretation dependencies; EXECUTE re-verifies every floor from its own data.

### 7.1 Window census (`probe_live.py` sha256 `c100f1775a8c367f69847948685d7303492e835014395a36bc47f47793361efe`; raw `census.json` sha256 `b0b9e5203380934e290a8f02ff585dd21cc7f96897cf552bf559b32917af96b0`)

Full frozen 57, two cold-GET sweeps ≈ 132 s apart (delta 131.8 s), plus an 8-GET burst on the 5 rate-capable endpoints and one short recovery probe. Observed sweep-0 and sweep-1 histograms are **identical**: `{BLOCK_403_CHALLENGE: 5, TRANSPORT_ERROR: 1, OTHER_NONBARRIER: 5, CLEAN: 46}`; no ambient class changed between the two sweeps. The **6 stably persistent T0 intrinsic barriers** are `gitlab.com/users/sign_in`, `community.cloudflare.com/`, `www.npmjs.com/login`, `wordpress.com/log-in`, `www.phpbb.com/community/` (all `BLOCK_403_CHALLENGE`) and `community.invisioncommunity.com/` (`TRANSPORT_ERROR`, DNS-unresolvable from this egress). `n_t0_intrinsic = n_t0_barrier = 6`, `f_b_obs ≈ 6/57 = 0.105`.

### 7.2 Recovery and newly-blocking reachability (live)

Bursts on `stratum_stress`: `www.djangoproject.com/accounts/login/` produced `RATE_LIMIT_429` at positions 4 and 7 and `search.brave.com/search?q=test` produced `RATE_LIMIT_429` at positions 1, 5 and 6 (`load_class = RATE_LIMIT_429`); `www.djangoproject.com/admin/login/`, `auth0.com/` stayed `CLEAN`; `community.home-assistant.io/` stayed `OTHER_NONBARRIER`. A short cold re-probe after the burst returned `CLEAN` for both 429-induced endpoints, so a **newly-blocking** endpoint is reachable under load and a rate-driven barrier **recovers** under ambient re-observation. Parent accepted evidence independently recorded 13 `RECOVERY` events and rate-limit onsets on the same stratum.

### 7.3 Live oracle liveness

`PC_ORACLE_BARRIER`: httpbin 429 → `RATE_LIMIT_429`, httpbingo 429 → `RATE_LIMIT_429`, `no-such-host.invalid` → `TRANSPORT_ERROR`, httpbin 403 → `UNAVAILABLE_403`. `NC_CLEAN_ORACLE`: httpbin 200/uuid and `example.com` → `CLEAN`.

### 7.4 Arithmetic floors and certificate verdict

- `n_t0_intrinsic ≥ 3` and `n_t0_barrier ≥ 3` are certified reachable (observed 6 and 6).
- `S1` floor: with `n_t0_intrinsic ≥ 3` and all intrinsic classes persisting, `STATIONARITY_SKILL = H(B_T0) ≥ H(3/57) ≈ 0.206 nats > 0.05` and the permutation p is `< alpha` under the PC calibration, so `STAT_SIG` follows from persistence.
- `S0` reachability: intrinsic break, intrinsic-denylist violation, and `STAT_SIG` false are each independently producible (rows `INTRINSIC_BREAK` and `NC_EXCHANGE` above). `FALSE_ACCEPT > 0.20` is reachable with any recovery among `n_t0_intrinsic ≥ 3` (`≥ 0.33`); a load-induced onset provides `FALSE_REJECT > 0`.
- Class-conditional reachability: the pre-freeze census observed load-induced `RATE_LIMIT_429` on `www.djangoproject.com/accounts/login/` and `search.brave.com/search?q=test` that recovered to `CLEAN`, so Q3 is measurable; if EXECUTE observes no load-induced 429 it reports `CLASS_CONDITIONAL_TRANSIENCE` as unmeasured without invalidating S1/S0.

**Certificate verdict: SATISFIED.** Both persistently-blocked and recovering/newly-blocking endpoints are reachable across separated windows, so the experiment proceeds rather than parking. If EXECUTE cannot re-verify the floors the packet is `MEASUREMENT_INVALID` (the operational analogue of PARK).

## 8. Controls

- `PC_SYNTHETIC_STATIONARY` (offline, R=300, seed 38074818597): power to select `S1` must be `>= 0.80`; fresh 295/300 (rho=0.98) and 263/300 (rho=0.92).
- `NC_SYNTHETIC_EXCHANGEABLE` (offline, R=300, seed 38074818598): full-`STAT_SIG` false-positive ≤ 0.05 required; fresh 0.0067.
- `PC_ORACLE_BARRIER` (live, `per_host_requests = 2`): each oracle request classified into its expected class; otherwise `MEASUREMENT_INVALID`.
- `NC_CLEAN_ORACLE` (live): all requests classify `CLEAN`; otherwise `MEASUREMENT_INVALID`.
- `C_PROBE_SELF_INDUCTION` (validity control, not a statistical null): ambient barrier prevalence across rungs for the 52 non-stress endpoints plus `STATIONARITY_SKILL_NO_STRESS`; a trend whose clustered CI excludes 0 is disclosed as a self-induction caveat.

Classifier replay must yield 0 mismatches re-deriving every class from stored fields. Any control failure / unreachable network (including BOTH 429 oracles challenged) / non-reproducible classifier / T0 floors unmet / delta_ref actual `< 1500 s` ⇒ `status = MEASUREMENT_INVALID`, never a scientific negative. Absence of a load-induced `RATE_LIMIT_429` endpoint is **not** a `MEASUREMENT_INVALID` condition: Q3 is a secondary refinement, so `CLASS_CONDITIONAL_TRANSIENCE` is reported as unmeasured and the primary S1/S0 decision proceeds.

## 9. Treatment / policy liveness

Physics estimation experiment, no SPIDER treatment arm ⇒ `treatment_liveness = NOT_APPLICABLE` (Product-scoped). `POLICY_STATIC_DENYLIST_INTRINSIC` is a bounded deterministic function of `ambient_class` (`DENY` if in `intrinsic_classes` else `ALLOW`) with a re-probe at `DENYLIST_HORIZON`; `POLICY_CLASS_CONDITIONAL_DENYLIST` is defined whenever `CLASS_CONDITIONAL_TRANSIENCE` holds. Both return a valid decision for every class and terminate.

## 10. Validity threats (disclosed)

1. **Single network vantage** — mandate's source-vantage axis not varied; one egress. Declared scope boundary.
2. **Window censoring** — horizon censored at `delta_ref = 1800 s`.
3. **Weak-effect underpowering at delta_SKILL** — a world whose true MI is exactly `0.05` nats is only ~0.6-powered; hence `STAT_SIG` uses the three-part conjunction, and the PC calibration shows strong persistence is fully powered. `S0` via `STAT_SIG` false alone is disclosed as an ambiguous-negative route; the two positive-change routes (`INTRINSIC_PERSISTENT` false, denylist violation) are unambiguous.
4. **Self-induced 429** — `C_PROBE_SELF_INDUCTION` and the 52 unstressed endpoints isolate induced load; `RATE_*`/`AMBIENT_RATE_*` never gate a primary branch.
5. **Coarse FA resolution** — smallest non-zero FA is `1/n_intrinsic`; `tau_FA = 0.20` tolerates one recovery among 5 but not two, so the horizon is a reported product quantity decoupled from the primary branch.
6. **Coarse intrinsic-persistence resolution** — with `n_intrinsic ≈ 6`, `CLASS_PERSISTENCE ≥ 0.80` requires all but one to persist; one flaky intrinsic endpoint routes `S1` to `S0`.
7. **Permutation vs. clustering** — the global shuffle does not preserve registrable-domain clusters; clustering is addressed by the bootstrap CI.
8. **Single-sample ambient state** — the ambient class is one GET per sweep; stochastic rate noise can read as an onset/recovery, which `AMBIENT_*` counters expose.
9. **`/tmp` provenance** — pre-freeze census/calibration scripts are not in the repo and are not interpretation dependencies; EXECUTE re-derives all floors and calibrations.
10. **Pre-freeze census is outcome-adjacent pilot** — it observes the same phenomenon on the same endpoints; endpoints are parent-inherited (not census-selected), it is the sanctioned attainability certificate, and it is not the frozen 4-sweep/1800 s measurement. The census proves the barrier *classes* are reachable and that a rate-limit barrier is inducible and recoverable; it does **not** certify persistence at 1800 s. Persistence at the frozen rungs is the quantity under test: if an intrinsic barrier present at T0 decays by 1800 s, that is a genuine `S0` positive-change result, not a measurement defect. AUDIT should note the census as a pilot, not a confirmation.

## 11. Product consequences

- **S1_STATIONARY:** a static intrinsic-access denylist built at one window remains valid through the tested horizon (≥ 1800 s, right-censored) on this pool; adopt `POLICY_STATIC_DENYLIST_INTRINSIC` with the measured `DENYLIST_HORIZON` as a quantified re-probe interval. If `CLASS_CONDITIONAL_TRANSIENCE` also holds, adopt `POLICY_CLASS_CONDITIONAL_DENYLIST`: deny persistently-intrinsic endpoints and apply a short cool-down (from `RATE_RECOVERY_HALF_LIFE`) to `RATE_LIMIT_429` endpoints instead of denying them.
- **S0_NON_STATIONARY:** the endpoint intrinsic access decision is not amortizable through `delta_ref` on this pool/vantage; the dead-end policy must re-observe before relying on a cached per-endpoint decision, and no long static denylist horizon is licensed.

Either way the finding is bounded to this frozen pool, one network vantage and one window, and bounds (does not close) the timescale axis of C-WEB-DYNAMICS.

## 12. Provenance / code binding

`freeze_artifacts = []`; `freeze_artifacts_bound = NOT_APPLICABLE`. No mutable local code, task bank, dataset or fixture determines the interpretation. Every interpretation-determining constant is embedded verbatim in `spec.json` and this file, which the deterministic freezer hashes: the 57-endpoint universe (written literally), the challenge-marker regex and full intrinsic classifier (written literally), the sweep/induced protocol, strata, thresholds, seeds and branch precedence. The EXECUTE collection/analysis code does not exist at freeze and is authored at EXECUTE strictly as a literal realization of those embedded constants, with its hash recorded in `provenance.json` for AUDIT. Remote Web responses cannot be frozen; their target identifiers and sampling protocol are frozen in `spec.json`/prereg.md instead. The DESIGN-local pre-freeze probe scripts and outputs live in `/tmp` and are deliberately **not** interpretation dependencies (EXECUTE re-derives every quantity and floor from its own raw data). The inherited universe/classifier are reproduced literally rather than read from another packet at run time; EXECUTE must not import the parent numpy-dependent lib.

## 13. Non-duplication statement (pre-2.0)

`LEGACY: DISTINCT_EXTENSION` (Director mandate). The pre-2.0 `frontier/web-physics-volatility-freshness` program (sha `3bc393fc8d3c5fc2515da6e8c7481b2618fefdbe`; prereg sha `f4cf72f72a07033608dda5a68c99cd6e13e07fd8`; blob `9bb76113aeaf46d9aecdd8a38349a3a7741e57c3`) studied **content volatility/freshness over time windows** and closed `PAUSE_CLOSE_NEGATIVE` on structural data-insufficiency; it did not measure access-barrier class persistence or a denylist false-accept horizon. Within Research 2.0, `EXP-PHYSICS-37992957068` measured **next-request** barrier classification in a **single** window and bounded that sub-thread. This experiment changes the object (endpoint state persistence across a window ladder), the deliverable (a class-conditional validity horizon / re-probe interval) and the branch structure, and does not re-run next-request classification, value derivation/PMI, Graph `C-FRESHNESS` or Runtime drift controls.
