# EXP-PHYSICS-38074818597 — Preregistration (frozen before execution)

Lane: **physics**. Target claim: **C-WEB-DYNAMICS**. Director mandate action: **REOPEN**, cognitive reset, `parent_handoff_disposition` **USE**. `design_contract_version=2`.

This document is frozen together with `spec.json`; `spec.json` is the machine-binding source. Where wording differs, `spec.json` governs. Do not edit after `freeze.json` exists.

## 1. What is tested

On the frozen 57-endpoint credential-free HTTP GET universe (inherited verbatim from `EXP-PHYSICS-37992957068`, which inherited it from `EXP-PHYSICS-37973239386`; **not extended**, because the pre-freeze attainability certificate is satisfied inside the frozen 57), we measure the **persistence/timescale of each endpoint's intrinsic ACCESS-BARRIER state** across a ladder of separated observation windows, and the **validity horizon of a static endpoint-level denylist**.

This deliberately changes the unit of study from *next-request* barrier classification (bounded by `EXP-PHYSICS-37992957068`) to *endpoint access-state persistence across windows*. It is orthogonal to:

- the exhausted next-request / value-derivation / PMI sub-threads of physics;
- Graph `C-FRESHNESS` (staleness of inherited *content*);
- Runtime `C-MEAS-VALID` drift controls.

The temporal/window axis is measured. The mandate's **source-vantage** axis is **not** varied: this instrument has a single network egress vantage, which is a declared scope boundary, not a hidden generalization.

Two scientific outcomes are frozen and both are reachable:

- **S1_STATIONARY**: anchor state is informative at `delta_ref=1800 s` (STATIONARITY_SKILL >= 0.05 nats, permutation p < 0.05, clustered CI lower > 0) and the static denylist keeps FA <= 0.10 and FR <= 0.10 through the whole ladder (DENYLIST_HORIZON = 1800).
- **S0_NON_STATIONARY**: the denylist fails already at the first lag (FA(20s) > 0.10 or FR(20s) > 0.10, i.e. IMMEDIATE_FAIL), or the anchor carries no information about the lag (not STAT_SIG with MI_POWER_OK).
- **SM_CLASS_CONDITIONAL**: anchor is informative, intrinsic non-rate barriers persist (CLASS_PERSISTENCE >= 0.90) while rate-driven barriers recover, so validity is class-conditional.
- **SIN_INCONCLUSIVE**: anything else (notably an underpowered identity test with no immediate recovery).

`MEASUREMENT_INVALID` is reserved exclusively for prerequisite/control failure and must never be reported as a scientific negative.

## 2. Frozen intrinsic classifier (response-intrinsic, no history leakage)

Each response is classified from its own stored fields only (status, `cf-mitigated`, first 20000 body bytes, error string):

| class | rule |
|---|---|
| `CLEAN` | HTTP status in {200,202} and body does not match `CHALLENGE_RE` |
| `RATE_LIMIT_429` | HTTP status == 429 |
| `BLOCK_403_CHALLENGE` | HTTP status == 403 and (`lower(cf-mitigated) == "challenge"` **or** body matches `CHALLENGE_RE`) |
| `UNAVAILABLE_403` | HTTP status == 403 without any challenge marker |
| `TRANSPORT_ERROR` | no HTTP response (DNS/connect/TLS/timeout) |
| `OTHER_NONBARRIER` | any other HTTP status (404, 500, redirect chains to error, …) |

**Literal challenge regex (frozen once, fixing a provenance gap in the parent packet):**

```
CHALLENGE_RE_LITERAL = (?i)(just a moment|cf-chl|challenge-platform|checking your browser|cf_chl|turnstile|hcaptcha|captcha|attention required)
```

`CHALLENGE_RE` is applied to the first 20000 body bytes decoded as latin-1 (lossless byte mapping). `cf-mitigated` is lowercased and compared to the string `challenge`.

`barrier_set = {RATE_LIMIT_429, BLOCK_403_CHALLENGE, TRANSPORT_ERROR}`.
`ordinary_unavailability_set = {UNAVAILABLE_403, OTHER_NONBARRIER}`.
Severity rank (for load bursts): `TRANSPORT_ERROR 5 > RATE_LIMIT_429 4 > BLOCK_403_CHALLENGE 3 > UNAVAILABLE_403 2 > OTHER_NONBARRIER 1 > CLEAN 0`.

Every request stores raw status, `server`, `cf-mitigated`, `retry-after`, body SHA-256, byte length, first 20000 bytes, elapsed ms, sweep index, attempt index, endpoint and error string, so AUDIT recomputes the class deterministically. Classes depend only on a single request, so conditioning on the anchor state is not label leakage.

## 3. Frozen sweep protocol and strata

**Unit**: `(endpoint, sweep_index)`; anchor = sweep 0.

**Ladder** (target offsets from run start, seconds): `[0, 20, 120, 600, 1800]`; `delta_ladder = [20, 120, 600, 1800]`; `delta_ref = 1800`. Actual elapsed deltas are recorded; if a sweep overruns, its actual delta is used.

**Ambient probe (primary state)** — for EVERY endpoint: a fresh cookie jar, then exactly **one** HTTP GET. `ambient_class` = classifier output. Endpoints are probed sequentially in a **per-sweep frozen seeded permutation order** (seed `38074818597`) with inter-endpoint gap 0.30 s.

**Load probe (transient-class diagnostic only)** — immediately AFTER its ambient probe, each endpoint in `stratum_stress` receives a burst of **B_stress = 8** GETs at gap 0.15 s inside a **separate** fresh cookie jar. `load_class` = argmax severity rank over the 8 responses. The other 52 endpoints get no load probe.

**Primary state for all stationarity/denylist metrics is `ambient_class`.** `load_class` is used only for `TRANSIENT_RECOVERY_HALF_LIFE` / `STRESS_FALSE_ACCEPT`.

**Requests**: GET only; one frozen User-Agent (`SPIDER-research2/1.0 (+credential-free access-state persistence probe)`) and `Accept: */*`; no authentication; no JavaScript; no credentials.

**`stratum_stress`** (fixed pre-registered rate-limit-capable set, NOT chosen from this run's outcomes): `https://www.djangoproject.com/admin/login/`, `https://www.djangoproject.com/accounts/login/`, `https://auth0.com/`, `https://search.brave.com/search?q=test`, `https://community.home-assistant.io/`.

**`stratum_intrinsic_candidates`** (fixed pre-registered towards-persistent candidates): `https://gitlab.com/users/sign_in`, `https://community.cloudflare.com/`, `https://www.npmjs.com/login`, `https://wordpress.com/log-in`, `https://www.phpbb.com/community/`, `https://community.invisioncommunity.com/`.

## 4. Metrics, baselines and stable identifiers

- `STATIONARITY_SKILL` (**primary**) = plug-in binary mutual information `I(B_anchor; B_delta)` over the ambient barrier indicator, in nats/endpoint, at `delta_ref`; `B_EXCHANGE` endpoint-permutation p-value (10000 permutations, seed 38074818597); endpoint-clustered bootstrap 95% CI (cluster = registrable domain, 10000 resamples, seed 38074818597). `STATIONARITY_SKILL_BY_LAG` reports each ladder rung.
- `STATIONARITY_SKILL_MULTI` = 6-class plug-in MI `I(C_anchor; C_delta)` with the same null.
- `DENYLIST_FALSE_ACCEPT(delta)` = fraction of T0 ambient-barrier endpoints that are non-barrier at `delta` (denylisted endpoint recovered). `DENYLIST_FALSE_REJECT(delta)` = fraction of T0 ambient-nonbarrier endpoints that are barrier at `delta` (clean endpoint newly blocks).
- `DENYLIST_HORIZON` = largest ladder delta `delta_k` such that FA and FR pass at **every** lag up to and including `delta_k` (a contiguous valid prefix; a mid-ladder failure cannot be masked by a later pass), else 0. `DENYLIST_FIRST_FAIL_LAG` = smallest delta at which FA > 0.10 or FR > 0.10.
- `CLASS_PERSISTENCE` (per class) = fraction of endpoints with that T0 ambient class whose `delta_ref` ambient class is identical.
- `TRANSIENT_RECOVERY_HALF_LIFE` = for `stratum_stress`, smallest ladder delta at which the ambient class is non-barrier after a T0 `load_class` in `barrier_set` (per-endpoint + median). `STRESS_FALSE_ACCEPT` = fraction of those endpoints ambient-non-barrier at `delta_ref`.
- `DENYLIST_SKILL` = log-loss improvement (nats/endpoint) of the anchor-transfer predictor over `B_CONSTANT_USABLE` at `delta_ref`.
- `ONSET_n`, `RECOVERY_n`, `PERSIST_n` = ambient transition counts.

Baselines: `B_EXCHANGE` (mandated memory/constant null, permutation), `B_CONSTANT_USABLE` (always-usable floor), `B_MARGINAL`, `B_LASTSWEEP` (recent-memory diagnostic).

Stable ids: primary metric `STATIONARITY_SKILL`; baselines `B_EXCHANGE, B_CONSTANT_USABLE, B_MARGINAL, B_LASTSWEEP`; controls `PC_SYNTHETIC_STATIONARY, PC_ORACLE_BARRIER, NC_SYNTHETIC_EXCHANGEABLE, NC_CLEAN_ORACLE, C_PROBE_LOAD`; policy `POLICY_STATIC_DENYLIST`; classes `CLEAN, RATE_LIMIT_429, BLOCK_403_CHALLENGE, UNAVAILABLE_403, TRANSPORT_ERROR, OTHER_NONBARRIER`; branches `S1_STATIONARY, S0_NON_STATIONARY, SM_CLASS_CONDITIONAL, SIN_INCONCLUSIVE, MEASUREMENT_INVALID`.

Seeds: probe_order/bootstrap/permutation/pc_synthetic = 38074818597; nc_synthetic = 38074818598.

## 5. Null calibration (pre-freeze, non-outcome-bearing)

The mandated memory/constant null is `B_EXCHANGE`: shuffle the lag labels across endpoints (preserving anchor marginals and endpoint clusters) and recompute `I(B_anchor; B_delta)`. This is exactly the statement that the identity-transfer predictor is no better than the constant-marginal predictor.

Calibration ran the **actual** plug-in-MI + permutation statistic on synthetic data (no Web data), with N=57 endpoints, R=200 replications, 1000 permutations per replication (`/tmp/opencode/phys380/calib2.py`):

| control | configuration | frozen bound | achieved |
|---|---|---|---|
| `NC_SYNTHETIC_EXCHANGEABLE` | independent anchor/lag, p=0.20 | FP <= 0.05 | **0.01** |
| `NC_SYNTHETIC_EXCHANGEABLE` | independent anchor/lag, p=0.30 | FP <= 0.05 | **0.03** |
| `PC_SYNTHETIC_STATIONARY` | f_b=0.20, rho=0.80 | power >= 0.80 | **1.00** |
| `PC_SYNTHETIC_STATIONARY` | f_b=0.10, rho=0.80 | power >= 0.80 | **1.00** |
| `PC_SYNTHETIC_STATIONARY` | f_b=0.10, rho=0.50 (disclosed corner) | (informational) | 0.735 (**underpowered**) |
| `PC_SYNTHETIC_STATIONARY` (persistent-barrier reference) | f_b=0.05, rho=1.0 | power >= 0.80 | **0.92** |
| `PC_SYNTHETIC_STATIONARY` (persistent-barrier reference) | f_b=0.08, rho=1.0 | power >= 0.80 | **0.995** |
| `PC_SYNTHETIC_STATIONARY` (persistent-barrier reference) | f_b=0.10, rho=1.0 | power >= 0.80 | **1.00** |
| `PC_SYNTHETIC_STATIONARY` (persistent-barrier reference) | f_b=0.20, rho=1.0 | power >= 0.80 | **1.00** |

The underpowered corner is disclosed and is exactly why the STATIONARY branch requires `MI_POWER_OK` = power of the frozen PC generator at the **observed** `f_b_obs` under the **persistent-barrier reference regime `rho=1.0`** (motivated by the census's perfectly persistent intrinsic barriers) >= 0.80. An underpowered non-significant identity test is reported as `SIN_INCONCLUSIVE`, never as `S0`.

This calibrates the estimator and the null; it does not assert that any real endpoint is stationary.

## 6. Attainability certificate (pre-freeze, non-outcome-bearing)

All pre-freeze activity is non-confirmatory, offline-from-the-frozen-design, and establishes only reachability + calibration. The raw scripts are under `/tmp/opencode/phys380/` and are **not** a frozen interpretation dependency; EXECUTE re-verifies every floor from its own data.

### 6.1 Window-pair census (`census.py`)

17 fixed endpoints (all in the frozen 57), two sweeps separated by **45 s**, 3 GETs per endpoint per sweep at gap 0.3 s, plus a 6-GET/0.15 s burst on the 5 rate-limit-capable endpoints.

Over sweep A (51 requests): `{CLEAN 31, BLOCK_403_CHALLENGE 15, TRANSPORT_ERROR 3, RATE_LIMIT_429 2}`.
Over sweep B (51 requests): `{CLEAN 33, BLOCK_403_CHALLENGE 15, TRANSPORT_ERROR 3}`.
Burst (30 requests): `{CLEAN 29, RATE_LIMIT_429 1}`.

Modal A→B transitions over the 17 endpoints: **6 persistent** (5 `BLOCK_403_CHALLENGE`: gitlab.com/users/sign_in, community.cloudflare.com, www.npmjs.com/login, wordpress.com/log-in, www.phpbb.com/community/; 1 `TRANSPORT_ERROR`: community.invisioncommunity.com), **1 recovery** (`search.brave.com/search?q=test` `RATE_LIMIT_429 -> CLEAN` across the pair), **0 ambient onset**, 10 `CLEAN -> CLEAN`.

All 6 persistent endpoints and the recovering endpoint are inside the frozen 57.

### 6.2 Onset reachability probe (`onset.py`)

14 GETs at 0.12 s gap on 4 rate-limit-capable endpoints produced live **newly-blocking (onset)** events: `www.djangoproject.com/admin/login/` `200…200 429 200 200 200 429`; `accounts/login/` `200…429…429…`; `auth0.com/` `200…200 429/cf 429/cf 429/cf 429/cf`; `search.brave.com/search?q=test` alternates `429/200`. Recovery after 10 s: admin `200`, accounts `200`, brave `200`, auth0 `429`.

### 6.3 Branch reachability through the actual metric (`calib2.py`)

| synthetic plant | STATIONARITY_SKILL | perm p | FA | FR | branch |
|---|---|---|---|---|---|
| stationary (6 persistent barriers / 57) | 0.3365 | 0.001 | 0.00 | 0.00 | **S1** reachable |
| non-stationary (3 T0 barriers all recovered by T1) | 0.0 | 1.0 | 1.00 | 0.00 | **S0** reachable |
| class-conditional (6 persistent + 3 recovering) | 0.2360 | 0.001 | 0.333 | 0.00 | **SM** reachable |

### 6.4 Arithmetic lower bounds for the frozen run

Using only census-guaranteed persistent endpoints (no transient assumptions):

- T0 ambient-barrier endpoints >= **6** (the 5 persistent 403-challenge + 1 persistent transport), so `n_denylisted >= 6` and the prerequisite floor of 3 is satisfied. `f_b_obs` ~= 6/57 = 0.105, at which the frozen PC keeps power 1.00 under the persistent-barrier reference `rho=1.0` (>= 0.80), so `MI_POWER_OK` is attainable.
- `FA > 0.10` is reachable because `search.brave.com` recovered across the 45 s pair (any single recovery with n_denylisted ~= 6 gives FA >= 0.17).
- `FR > 0` is reachable via the demonstrated load-induced onsets (djangoproject admin/accounts, auth0).
- `CLASS_PERSISTENCE[BLOCK_403_CHALLENGE] >= 0.90` and `CLASS_PERSISTENCE[TRANSPORT_ERROR] >= 0.90` are reachable because the 5 challenge endpoints and the transport endpoint were persistent across the 45 s pair.

**Certificate verdict: SATISFIED.** Both persistently-blocked endpoints and a recovering/newly-blocking endpoint are reachable across the window pair, so the experiment proceeds rather than parking. If EXECUTE cannot re-verify the >= 3 T0 ambient-barrier floor (or the anchor/delta_ref sweeps), the packet is `MEASUREMENT_INVALID`, which is the operational analogue of the mandate's PARK.

## 7. Controls

- `PC_SYNTHETIC_STATIONARY` (offline, f_b=0.20, rho=0.80, R=200, seed 38074818597): power >= 0.80 required, achieved 1.00; `MI_POWER_OK` also computed at `f_b_obs`.
- `NC_SYNTHETIC_EXCHANGEABLE` (offline, p=0.20, R=200, seed 38074818598): false-positive <= 0.05 required, achieved 0.01.
- `PC_ORACLE_BARRIER` (live): `httpbin.org/status/429` → `RATE_LIMIT_429`; `no-such-host.invalid` → `TRANSPORT_ERROR`; `httpbin.org/status/403` → `UNAVAILABLE_403`.
- `NC_CLEAN_ORACLE` (live): `httpbin.org/status/200`, `httpbin.org/uuid` → `CLEAN`.
- `C_PROBE_LOAD` (validity control): Cochran-Armitage trend of ambient barrier prevalence across sweeps for the 52 non-stress endpoints; a rising trend is disclosed as self-induction.
- Classifier replay must yield 0 mismatches re-deriving every class from stored fields.

Any control failure / unreachable network / non-reproducible classifier / T0 floor below 3 ⇒ `status = MEASUREMENT_INVALID`.

## 8. Decision rule

See `spec.json.decision_rule`. Thresholds: `tau_FA = tau_FR = 0.10`, `alpha = 0.05`, `delta_SKILL = 0.05` nats, PC power >= 0.80, NC FP <= 0.05, T0 ambient-barrier floor >= 3, 10000 permutations/resamples.

Gates: `STAT_SIG = STAT_SIG_SIGONLY AND MI_POWER_OK`, where `STAT_SIG_SIGONLY = (STATIONARITY_SKILL(1800) >= 0.05) AND (perm p < 0.05) AND (clustered CI lower > 0)` and `MI_POWER_OK` = PC power at the observed `f_b_obs` under the persistent-barrier reference `rho=1.0` >= 0.80. `IMMEDIATE_FAIL = DENYLIST_HORIZON == 0` (the contiguous valid prefix is empty); `INTRINSIC_PERSISTENT`; `TRANSIENT_UNSTABLE`.

Branch precedence: `MEASUREMENT_INVALID` → `S0_NON_STATIONARY` (`IMMEDIATE_FAIL` OR (`MI_POWER_OK` AND NOT `STAT_SIG_SIGONLY`)) → `S1_STATIONARY` (`STAT_SIG` AND horizon 1800) → `SM_CLASS_CONDITIONAL` (`STAT_SIG` AND partial horizon AND `INTRINSIC_PERSISTENT` AND `TRANSIENT_UNSTABLE`) → `SIN_INCONCLUSIVE`.

Claim ceiling: C-WEB-DYNAMICS remains **HYPOTHESIS**; S0/SM bound (do not reject) a pooled static-denylist prior on this pool/window; no PRODUCT_CORE promotion and no EXPERIMENTAL upgrade from a single window ladder.

## 9. Treatment / policy liveness

`POLICY_STATIC_DENYLIST` is a bounded deterministic function of `ambient_class`: `DENY` if `ambient_class in barrier_set` else `ALLOW`, with a deterministic re-probe at `DENYLIST_HORIZON`. EXECUTE's first action is a **non-network** policy trace proving a defined decision for every class and termination (recorded in `provenance.json`). This is a Physics estimation experiment, not a Product inheritance arm, so no SPIDER treatment-liveness substitution is claimed.

## 10. Validity threats (disclosed)

1. **Single network vantage.** The mandate's source-vantage axis is not varied; results are one egress. Explicit scope boundary against over-generalization.
2. **Window censoring.** The horizon is censored at `delta_ref = 1800 s`; timescales beyond 30 minutes are not measured.
3. **Self-induced 429.** Single ambient GETs may still accumulate barriers; `C_PROBE_LOAD` measures the trend, `stratum_stress` isolates induced load, and the 52 unstressed endpoints are the clean persistence substrate.
4. **Coarse FA resolution.** The smallest non-zero FA is `1/n_denylisted (~0.17)`; `tau_FA = 0.10` therefore flags the horizon as failed on **any** recovery. This is conservative and favors the product-safe reading.
5. **Pool composition.** Persistent 403-challenge endpoints dominate the pooled MI and can mask rate-driven non-stationarity; the class-conditional metrics and `STATIONARITY_SKILL_MULTI` guard against dilution.
6. **Low-prevalence power.** If the run's `f_b_obs` is low, `MI_POWER_OK` may be false; then STATIONARY cannot be claimed and the result defaults to `SM`/`SIN`, not a false `S0`.
7. **Live oracles** depend on third-party hosts; oracle failure is a measurement-invalid signal, not a negative.
8. **`/tmp` provenance.** Pre-freeze census/probe artifacts are not persisted in the repo and are not interpretation dependencies; EXECUTE must re-derive all floors from its own collected data (AUDIT should treat the census summary here as explanatory, not as frozen evidence).

## 11. Product consequences

- **Positive (S1):** a static endpoint denylist is valid through >= 1800 s on this pool; adopt terminal classification with the measured `DENYLIST_HORIZON` as the re-probe interval; no online per-endpoint history model is needed for access decisions.
- **Negative (S0 / SM):** a pooled static denylist silently goes stale (false-accept on recovered endpoints; false-reject on newly blocked endpoints). Split the dead-end policy into an intrinsic-block track with a long horizon and a rate-driven track driven by `TRANSIENT_RECOVERY_HALF_LIFE` / `STRESS_FALSE_ACCEPT`, or treat endpoint access state as non-amortizable and re-observe before use. This bounds the timescale axis of C-WEB-DYNAMICS on this pool/window.

## 12. Provenance / code binding

No mutable local fixture, task bank, dataset or pre-existing code file is an interpretation dependency; therefore `freeze_artifacts` is empty and `freeze_artifacts_bound` is `NOT_APPLICABLE`. All interpretation-determining constants are embedded in `spec.json` and this file, which the deterministic freezer hashes (`freeze.json.hashes.spec.json`, `prereg.md`). EXECUTE must implement the collection/analysis code strictly as a literal realization of these literals, must not introduce or retune any decision-relevant constant, and must record the code hash in `provenance.json` for AUDIT.

## 13. Non-duplication statement

This experiment does **not** re-run next-request barrier classification or an adaptive-vs-retry request economy (`EXP-PHYSICS-37992957068`), value derivation / PMI sub-threads, Graph `C-FRESHNESS` (content staleness), or Runtime `C-MEAS-VALID` drift controls. Its object is the endpoint's server-side access-decision process over time (barrier persistence/recovery) and the resulting static-denylist validity horizon.
