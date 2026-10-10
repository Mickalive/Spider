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

### 1.1 The branch design (materially changed from the prior single-window, next-request design)

Two deliberate corrections over the prior draft:

1. The primary stationarity decision is made on **endpoint-identity information** (`STATIONARITY_SKILL`) and intrinsic-class persistence, **not** on the coarse pooled-denylist horizon. The pooled-denylist false-accept resolution is `1/n_denylisted` (≈0.11–0.17 here), so a *single* rate-driven recovery forces `DENYLIST_HORIZON=0`. If the horizon drove the primary branch, a genuinely class-conditional world (persistent intrinsic barriers + transient rate barriers) would be mislabelled `S0_NON_STATIONARY`. The fresh branch probe confirms the fix: a class-conditional plant yields `STATIONARITY_SKILL=0.2360`, `p=1e-4`, `FA=0.333`, `HORIZON=0`, intrinsic persistence `1.0` → `SM_CLASS_CONDITIONAL`, whereas horizon-first precedence would return `S0`.

2. `S0_NON_STATIONARY` is defined by **positive change evidence**, not by a non-significant MI test. A "powered non-significance" gate is unsound (non-significance is not evidence of no association; it is ambiguity), and a power reference at `rho=1.0` is vacuous given the ≥3-barrier floor. Therefore:
   - `INTRINSIC_BREAK` (a T0 intrinsic class failed to persist) **or** `STATE_CHANGE_EVIDENCE` with no intrinsic class at T0 ⇒ `S0`;
   - a merely non-significant `STATIONARITY_SKILL` with no positive change evidence ⇒ `SIN_INCONCLUSIVE`, never `S0`;
   - MI power (`MI_POWER_OK`, `POWER_AT_RHO90`, `POWER_AT_DELTA_SKILL`) is a **reported diagnostic**, not a branch gate.

Frozen dispositions (both scientific directions reachable; `MEASUREMENT_INVALID` reserved exclusively for prerequisite/control failure):

- **S1_STATIONARY**: `STAT_SIG_SIGONLY` AND `INTRINSIC_PERSISTENT` AND `NOT RATE_TRANSIENT` AND `NOT STATE_CHANGE_EVIDENCE`. `DENYLIST_HORIZON = 1800` is then an **implied reported consequence**, not a gate.
- **S0_NON_STATIONARY**: `INTRINSIC_BREAK` OR (`STATE_CHANGE_EVIDENCE` AND no intrinsic class at T0). Positive evidence that the barrier state changed.
- **SM_CLASS_CONDITIONAL**: `INTRINSIC_PERSISTENT` AND `RATE_TRANSIENT` (intrinsic non-rate barriers persist; rate-driven barriers recover/intermittently appear, so the re-probe interval is class-conditional).
- **SIN_INCONCLUSIVE**: otherwise (notably: intrinsic persists, no rate transience, but a non-rate state change; no intrinsic class at T0 and no change; or a non-significant MI test with no positive change evidence).

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
Intrinsic classes = `{BLOCK_403_CHALLENGE, TRANSPORT_ERROR}`.
Severity rank (for load bursts): `TRANSPORT_ERROR 5 > RATE_LIMIT_429 4 > BLOCK_403_CHALLENGE 3 > UNAVAILABLE_403 2 > OTHER_NONBARRIER 1 > CLEAN 0`.

Every request stores raw status, `server`, `cf-mitigated`, `retry-after`, body SHA-256, byte length, first 20000 bytes, elapsed ms, sweep index, attempt index, endpoint and error string, so AUDIT recomputes the class deterministically. Classes depend only on a single request, so conditioning on the anchor state is not label leakage.

## 3. Frozen sweep protocol and strata

**Unit**: `(endpoint, sweep_index)`; anchor = sweep 0.

**Ladder** (target offsets from run start, seconds): `[0, 20, 120, 600, 1800]`; `delta_ladder = [20, 120, 600, 1800]`; `delta_ref` = final sweep (nominal 1800). The **analysis labels each sweep by its nominal rung** and evaluates all per-rung metrics (`FA`/`FR`, `DENYLIST_HORIZON`, `DENYLIST_FIRST_FAIL_LAG`) on nominal rungs, so `DENYLIST_HORIZON ∈ {0, 20, 120, 600, 1800}`. The **actual** elapsed delta of each sweep is recorded and reported alongside the nominal rung and is used only for descriptive timing and for the `delta_ref` validity check: the final sweep's actual delta must be ≥ 1500 s or the run is `MEASUREMENT_INVALID`.

**Request policy (frozen, decision-relevant):** GET only, follow up to **5** redirects, **30 s** timeout (connect+read), **TLS verification on**, **no retries**, **one attempt per observation**. Because there is no retry, a DNS/connect/TLS/timeout failure is directly `TRANSPORT_ERROR` rather than a retried `CLEAN`. The stored `attempt_index` is 0 for all ambient and load observations. A frozen User-Agent (`SPIDER-research2/1.0 (+credential-free access-state persistence probe)`) and `Accept: */*` are sent; no authentication, JavaScript or credentials.

**Ambient probe (primary state)** — for EVERY endpoint: a fresh cookie jar, then exactly **one** HTTP GET. `ambient_class` = classifier output. Endpoints are probed sequentially in a **per-sweep frozen seeded permutation order** (seed `38074818597`) with inter-endpoint gap 0.30 s.

**Load probe (transient-class diagnostic only)** — immediately AFTER its ambient probe, each endpoint in `stratum_stress` receives a burst of **B_stress = 8** GETs at gap 0.15 s inside a **separate** fresh cookie jar. `load_class` = argmax severity rank over the 8 responses. The other 52 endpoints get no load probe.

**Primary state for all stationarity/denylist metrics is `ambient_class`.** `load_class` is used only for `TRANSIENT_RECOVERY_HALF_LIFE` / `STRESS_FALSE_ACCEPT`.

**`stratum_stress`** (fixed pre-registered rate-limit-capable set, NOT chosen from this run's outcomes): `https://www.djangoproject.com/admin/login/`, `https://www.djangoproject.com/accounts/login/`, `https://auth0.com/`, `https://search.brave.com/search?q=test`, `https://community.home-assistant.io/`.

**`stratum_intrinsic_candidates`** (fixed pre-registered towards-persistent candidates): `https://gitlab.com/users/sign_in`, `https://community.cloudflare.com/`, `https://www.npmjs.com/login`, `https://wordpress.com/log-in`, `https://www.phpbb.com/community/`, `https://community.invisioncommunity.com/`.

## 4. Metrics, baselines and stable identifiers

- `STATIONARITY_SKILL` (**primary**) = plug-in binary mutual information `I(B_anchor; B_delta)` over the ambient barrier indicator, in nats/endpoint, at `delta_ref`; `B_EXCHANGE` **global** endpoint-permutation p-value (10000 uniform shuffles of the lag vector across all 57 endpoints; seed 38074818597); endpoint-clustered bootstrap 95% CI (cluster = registrable domain, 10000 resamples, seed 38074818597). `STATIONARITY_SKILL_BY_LAG` reports each ladder rung; `STATIONARITY_SKILL_NO_STRESS` repeats the primary at `delta_ref` on the 52 non-stressed endpoints (self-induction robustness replica).
- `registrable_domain(url)` (frozen): take the URL host, strip a single leading `www.`, retain the final two dot-separated labels (no multi-label public suffix occurs in the frozen 57), e.g. `gitlab.gnome.org → gnome.org`, `www.djangoproject.com → djangoproject.com`.
- `STATIONARITY_SKILL_MULTI` = 6-class plug-in MI `I(C_anchor; C_delta)` with the same null.
- `DENYLIST_FALSE_ACCEPT(delta)` = fraction of T0 ambient-barrier endpoints that are non-barrier at `delta`. `DENYLIST_FALSE_REJECT(delta)` = fraction of T0 ambient-nonbarrier endpoints that are barrier at `delta`.
- `DENYLIST_HORIZON` = largest ladder delta `delta_k` such that FA and FR pass at **every** lag up to and including `delta_k` (a contiguous valid prefix), else 0. `DENYLIST_FIRST_FAIL_LAG` = smallest delta at which FA > 0.10 or FR > 0.10.
- `INTRINSIC_PERSISTENT` = at least one intrinsic class is present at T0 AND every present intrinsic class has `CLASS_PERSISTENCE ≥ 0.90`. `INTRINSIC_BREAK` = (an intrinsic class is present at T0) AND NOT `INTRINSIC_PERSISTENT`.
- `RATE_TRANSIENT` = `(STRESS_FALSE_ACCEPT > 0.10)` OR `(median TRANSIENT_RECOVERY_HALF_LIFE finite and < 1800)` OR `(a RATE_LIMIT_429 endpoint is present at T0 and CLASS_PERSISTENCE[RATE_LIMIT_429] < 0.90)` OR `(AMBIENT_RECOVERY_n > 0)` OR `(STRESS_ONSET_n > 0)`.
- `STATE_CHANGE_EVIDENCE` = `(AMBIENT_RECOVERY_n > 0)` OR `(AMBIENT_ONSET_n > 0)` OR `(DENYLIST_FALSE_ACCEPT(1800) > 0.10)` OR `(DENYLIST_FALSE_REJECT(1800) > 0.10)`.
- `CLASS_PERSISTENCE` (per class) = fraction of endpoints with that T0 ambient class whose `delta_ref` ambient class is identical.
- `TRANSIENT_RECOVERY_HALF_LIFE` = for `stratum_stress`, smallest **nominal** rung at which the ambient class is non-barrier after a T0 `load_class` in `barrier_set` (per-endpoint + median); if no `stratum_stress` endpoint has a T0 `load_class` in `barrier_set`, the median is `null` and the corresponding `RATE_TRANSIENT` term is false. `STRESS_FALSE_ACCEPT` = fraction of those endpoints ambient-non-barrier at `delta_ref`, defined as **0.0** when the denominator is empty.
- `DENYLIST_SKILL` = log-loss improvement (nats/endpoint) of the anchor-transfer predictor over `B_CONSTANT_USABLE` at `delta_ref`.
- `AMBIENT_ONSET_n`, `AMBIENT_RECOVERY_n`, `STRESS_ONSET_n`, `PERSIST_n` = ambient transition counts (`AMBIENT_RECOVERY_n` = barrier→non-barrier transitions between consecutive sweeps; `AMBIENT_ONSET_n` = non-barrier→barrier; `STRESS_ONSET_n` = ambient `RATE_LIMIT_429` appearances on `stratum_stress` endpoints whose T0 ambient class was not `RATE_LIMIT_429`; `PERSIST_n` = endpoints with identical ambient class at T0 and `delta_ref`).
- Power diagnostics (reported, non-gating): `POWER_AT_DELTA_SKILL` (power at MI = 0.05 nats at `f_b_obs`), `POWER_AT_RHO90` (power at `f_b_obs`, rho=0.90), `MI_POWER_OK` (power at `f_b_obs`, rho=1.0).

Baselines: `B_EXCHANGE` (**global** lag-label permutation null), `B_CONSTANT_USABLE` (always-usable floor), `B_MARGINAL`, `B_LASTSWEEP` (recent-memory diagnostic).

Stable ids: primary metric `STATIONARITY_SKILL`; baselines `B_EXCHANGE, B_CONSTANT_USABLE, B_MARGINAL, B_LASTSWEEP`; controls `PC_SYNTHETIC_STATIONARY, PC_ORACLE_BARRIER, NC_SYNTHETIC_EXCHANGEABLE, NC_CLEAN_ORACLE, C_PROBE_LOAD`; policies `POLICY_STATIC_DENYLIST, POLICY_CLASS_CONDITIONAL_DENYLIST`; classes `CLEAN, RATE_LIMIT_429, BLOCK_403_CHALLENGE, UNAVAILABLE_403, TRANSPORT_ERROR, OTHER_NONBARRIER`; branches `S1_STATIONARY, S0_NON_STATIONARY, SM_CLASS_CONDITIONAL, SIN_INCONCLUSIVE, MEASUREMENT_INVALID`.

Seeds: probe_order/bootstrap/permutation/pc_synthetic = 38074818597; nc_synthetic = 38074818598.

## 5. Null calibration (pre-freeze, non-outcome-bearing)

The mandated memory/constant null is `B_EXCHANGE`: a **global uniform shuffle** of the lag labels across all endpoints (anchor marginals preserved because only the lag vector is permuted; permutation clusters are **not** preserved — clustering is handled by the bootstrap), recomputing `I(B_anchor; B_delta)`. This is exactly the statement that the identity-transfer predictor is no better than the constant-marginal predictor.

Fresh calibration ran the **actual** plug-in-MI + permutation statistic on synthetic data (no Web data), with N=57 endpoints, R=200 replications, 1000 permutations per replication (`/tmp/opencode/phys380_cal/calib.py`, sha256 `c5860b9b5fedd41e0356b4553e49b4fe16debef98a02104a809d4b367c03e886`):

| control | configuration | frozen bound | fresh achieved |
|---|---|---|---|
| `NC_SYNTHETIC_EXCHANGEABLE` | independent anchor/lag, p=0.20 | FP ≤ 0.05 | **0.01** |
| `NC_SYNTHETIC_EXCHANGEABLE` | independent anchor/lag, p=0.30 | FP ≤ 0.05 | **0.03** |
| `PC_SYNTHETIC_STATIONARY` | f_b=0.20, rho=0.80 | power ≥ 0.80 | **1.00** |
| `PC_SYNTHETIC_STATIONARY` | f_b=0.10, rho=0.80 | power ≥ 0.80 | **0.985** |
| `PC_SYNTHETIC_STATIONARY` | f_b=0.10, rho=0.50 (disclosed corner) | (informational) | 0.81 (**marginal**) |

Minimum-meaningful-effect power (`/tmp/opencode/phys380_cal/power_min.py`, sha256 `84074980a49b624d42fe873be80d83d4c53b5866671bc6ef7c8f3e3d96d5a056`): for each `f_b` a generator whose true MI equals `delta_SKILL = 0.05` nats was constructed and the frozen test's power measured (N=57, R=200, 500 perms):

| `f_b` | rho* | true MI | power |
|---|---|---|---|
| 0.0526 | 0.475 | 0.0500 | **0.490** |
| 0.07 | 0.433 | 0.0500 | 0.525 |
| 0.10 | 0.392 | 0.0500 | 0.550 |
| 0.15 | 0.358 | 0.0500 | 0.585 |
| 0.20 | 0.340 | 0.0500 | 0.560 |
| 0.30 | 0.323 | 0.0500 | 0.555 |
| 0.40 | 0.316 | 0.0500 | 0.670 |

**Interpretation (frozen consequence):** at this n, a *weak-but-real* persistence (`MI ≈ 0.05`) is **not** reliably detectable (power ≈ 0.49–0.67), while a strong persistence (`rho ≈ 0.9–1.0`) is (power ≈ 0.97–1.00). Therefore an absence of significance cannot be used to claim non-stationarity. This is exactly why `S0` is defined by **positive change evidence** (`INTRINSIC_BREAK` / `STATE_CHANGE_EVIDENCE`) and why the power quantities are reported as diagnostics rather than used as a gate. The null/PC thresholds themselves (FP ≤ 0.05 at p=0.20; power ≥ 0.80 at f_b=0.20,rho=0.80) are unchanged and pass.

This calibrates the estimator and the null; it does not assert that any real endpoint is stationary.

## 6. Attainability certificate (pre-freeze, non-outcome-bearing)

All pre-freeze activity is non-confirmatory, offline-from-the-frozen-design, and establishes only reachability + calibration. The raw scripts are under `/tmp/opencode/phys380_cal/` and are **not** a frozen interpretation dependency; EXECUTE re-verifies every floor from its own data.

### 6.1 Window-pair census (`census.py`, sha256 `5050fdf28cfbf230a70492cae6514d10ba5fcf8405c6a8672557f5628bfd72e3`)

A fixed 26-endpoint subset of the frozen 57 (the 6 intrinsic candidates, the 5 rate-limit-capable candidates, and 15 ordinary endpoints), two sweeps separated by 30 s, one GET per endpoint per sweep at gap 0.30 s, plus a 6-GET/0.12 s burst on the 5 rate-limit-capable endpoints. Two independent census runs were executed.

Window-A class histogram over the 26 endpoints (both runs): `{BLOCK_403_CHALLENGE 5, TRANSPORT_ERROR 1, RATE_LIMIT_429 1, OTHER_NONBARRIER 2, CLEAN 17}`.

| run | persistent barriers (A→B) | recovery (A→B) | ambient onset | oracle_ok |
|---|---|---|---|---|
| run 1 | 6 (5 challenge + 1 transport) | 1 (`search.brave.com/search?q=test` `RATE_LIMIT_429 → CLEAN`) | 0 | true |
| run 2 | 7 (5 challenge + 1 transport + `search.brave.com` `RATE_LIMIT_429`) | 0 | 0 | true |

The 6 **stably persistent** endpoints across both runs: `gitlab.com/users/sign_in`, `community.cloudflare.com`, `www.npmjs.com/login`, `wordpress.com/log-in`, `www.phpbb.com/community/` (all `BLOCK_403_CHALLENGE`) and `community.invisioncommunity.com` (`TRANSPORT_ERROR`). The rate-limited endpoint `search.brave.com/search?q=test` varied run-to-run (`429→CLEAN` in one run, persistent `429` in the other) — a live demonstration of the class-conditional structure this experiment measures.

### 6.2 Onset reachability (same script)

The burst probe produced live, newly-blocking `RATE_LIMIT_429` events that clean single ambient GETs missed: `www.djangoproject.com/accounts/login/` sequence `CLEAN, 429, CLEAN, CLEAN, 429, CLEAN`; `search.brave.com/search?q=test` sequence `CLEAN, 429, CLEAN, CLEAN, CLEAN, CLEAN`. So a newly-blocking endpoint is reachable on this substrate; it is exposed reliably only under load, which is why the load probe is retained and the self-induction control `C_PROBE_LOAD` is pre-registered.

### 6.3 Branch reachability through the actual metric (`branch_probe2.py`, sha256 `0ffb401058e11e76c56dbeabbafe1c8c3e54b49a672ca649879adaee10afdb4d`)

| synthetic world | result | MI | perm p | INTRINSIC_PERSISTENT | RATE_TRANSIENT | STATE_CHANGE | FA | HORIZON | branch |
|---|---|---|---|---|---|---|---|---|---|
| stationary (6 persistent challenge + 1 transport) | | 0.3725 | 0.002 | true | false | false | 0.00 | 1800 | **S1** reachable |
| exchangeable (Bern 0.15 barrier/sweep; ≥3 T0 barriers, floor met) | INTRINSIC_BREAK | 0.0075 | 0.573 | false | true | true | 0.714 | 0 | **S0** reachable |
| class-conditional (6 persistent + 3 rate recovering) | | 0.2360 | 0.002 | true | true | true | 0.333 | 0 | **SM** reachable |
| intrinsic-persistent + generic (non-rate) onset | | 0.2861 | 0.002 | true | false | true | 0.00 | 1800 | **SIN** reachable |

The exchangeable world is routed to `S0` by **positive** change evidence (`INTRINSIC_BREAK`), not by its non-significant MI, confirming that no branch depends on a non-significant negative. `MEASUREMENT_INVALID` is produced only by prerequisite/control failure.

### 6.4 Arithmetic lower bounds for the frozen run

Using only census-guaranteed persistent endpoints (no transient assumptions):

- T0 ambient-barrier endpoints ≥ **6** (the 5 persistent 403-challenge + 1 persistent transport), so `n_denylisted ≥ 6` and the prerequisite floor of 3 is satisfied. `f_b_obs ≈ 6/57 = 0.105`, at which the frozen PC keeps power ≈ 0.995 under `rho=1.0` and ≈ 0.97 under `rho=0.90`; the diagnostic `MI_POWER_OK` is therefore reported as true, but no branch depends on it.
- `S1` is reachable: exact stationarity over the ladder (fresh probe: MI 0.3725, p 0.002).
- `S0` is reachable by positive change: any intrinsic-class recovery (fresh exchangeable probe: INTRINSIC_BREAK, FA 0.714).
- `SM` is reachable and, given the observed run-to-run rate variability, is an a-priori plausible real outcome: intrinsic barriers persist while a rate class recovers.
- `SIN` is reachable on a floor-satisfying pool: intrinsic barriers persist with only a non-rate change (fresh probe), or an intrinsic-persistent pool whose pooled MI is not significant.
- `FA > 0.10` is reachable (run 1 recovered `search.brave.com`; with `n_denylisted ≈ 6` any single recovery gives FA ≥ 0.17).
- `FR > 0` is reachable via the demonstrated load-induced onsets.
- `CLASS_PERSISTENCE[BLOCK_403_CHALLENGE] ≥ 0.90` and `CLASS_PERSISTENCE[TRANSPORT_ERROR] ≥ 0.90` are reachable because the 5 challenge endpoints and the transport endpoint were persistent across both census window pairs.

**Certificate verdict: SATISFIED.** Both persistently-blocked endpoints and a recovering/newly-blocking endpoint are reachable across the window pair, so the experiment proceeds rather than parking. If EXECUTE cannot re-verify the ≥3 T0 ambient-barrier floor (or the anchor/delta_ref sweeps), the packet is `MEASUREMENT_INVALID`, which is the operational analogue of the mandate's PARK.

## 7. Controls

- `PC_SYNTHETIC_STATIONARY` (offline, f_b=0.20, rho=0.80, R=200, seed 38074818597): power ≥ 0.80 required, fresh achieved 1.00; also reports `MI_POWER_OK`, `POWER_AT_RHO90`, `POWER_AT_DELTA_SKILL` as non-gating diagnostics.
- `NC_SYNTHETIC_EXCHANGEABLE` (offline, p=0.20, R=200, seed 38074818598): false-positive ≤ 0.05 required, fresh achieved 0.01.
- `PC_ORACLE_BARRIER` (live): `httpbin.org/status/429` → `RATE_LIMIT_429` (with `httpbingo.org/status/429` as a redundant 429 oracle); `no-such-host.invalid` → `TRANSPORT_ERROR`; `httpbin.org/status/403` → `UNAVAILABLE_403`.
- `NC_CLEAN_ORACLE` (live): `httpbin.org/status/200`, `httpbin.org/uuid`, `example.com` → `CLEAN`.
- `C_PROBE_LOAD` (validity control): Cochran-Armitage trend of ambient barrier prevalence across sweeps for the 52 non-stress endpoints, plus the `STATIONARITY_SKILL_NO_STRESS` replica; a rising trend or a large full-vs-no-stress gap is disclosed as self-induction.
- Classifier replay must yield 0 mismatches re-deriving every class from stored fields.

Any control failure / unreachable network (including BOTH 429 oracle hosts challenged/unreachable) / non-reproducible classifier / T0 floor below 3 / delta_ref actual delta < 1500 s ⇒ `status = MEASUREMENT_INVALID`.

## 8. Decision rule

See `spec.json.decision_rule`. Thresholds: `tau_FA = tau_FR = 0.10`, `alpha = 0.05`, `delta_SKILL = 0.05` nats, PC power ≥ 0.80, NC FP ≤ 0.05, intrinsic persistence ≥ 0.90, T0 ambient-barrier floor ≥ 3, 10000 permutations/resamples.

Gates:

- `STAT_SIG_SIGONLY = (STATIONARITY_SKILL(1800) ≥ 0.05) AND (perm p < 0.05) AND (clustered CI lower > 0)` — stationarity evidence.
- `INTRINSIC_PERSISTENT` = at least one intrinsic class present at T0 AND every present intrinsic class has `CLASS_PERSISTENCE ≥ 0.90`.
- `INTRINSIC_BREAK = (an intrinsic class is present at T0) AND NOT INTRINSIC_PERSISTENT`.
- `RATE_TRANSIENT = (STRESS_FALSE_ACCEPT > 0.10) OR (median TRANSIENT_RECOVERY_HALF_LIFE finite and < 1800) OR (a RATE_LIMIT_429 endpoint is present at T0 and CLASS_PERSISTENCE[RATE_LIMIT_429] < 0.90) OR (AMBIENT_RECOVERY_n > 0) OR (STRESS_ONSET_n > 0)`. Generic ambient onsets (`AMBIENT_ONSET_n`) are reported but deliberately excluded from this gate, because a new intrinsic block is consistent with intrinsic persistence and would otherwise mis-route to `SM`.
- `STATE_CHANGE_EVIDENCE = (AMBIENT_RECOVERY_n > 0) OR (AMBIENT_ONSET_n > 0) OR (DENYLIST_FALSE_ACCEPT(1800) > 0.10) OR (DENYLIST_FALSE_REJECT(1800) > 0.10)`.
- Power diagnostics `MI_POWER_OK`, `POWER_AT_RHO90`, `POWER_AT_DELTA_SKILL` are **reported only** and are not gates.

Branch precedence:

1. `MEASUREMENT_INVALID` (prerequisite/control failure only).
2. `S0_NON_STATIONARY` if `INTRINSIC_BREAK` OR (`STATE_CHANGE_EVIDENCE` AND no intrinsic class present at T0). A **positive** non-stationarity result.
3. `S1_STATIONARY` if `STAT_SIG_SIGONLY AND INTRINSIC_PERSISTENT AND NOT RATE_TRANSIENT AND NOT STATE_CHANGE_EVIDENCE`. (`DENYLIST_HORIZON = 1800` then follows as a reported consequence, since `NOT STATE_CHANGE_EVIDENCE` implies no ambient transitions and `FA`/`FR ≤ 0.10` at `delta_ref`.)
4. `SM_CLASS_CONDITIONAL` if `INTRINSIC_PERSISTENT AND RATE_TRANSIENT`.
5. `SIN_INCONCLUSIVE` otherwise (including a non-significant `STAT_SIG_SIGONLY` with no positive change evidence).

Claim ceiling: C-WEB-DYNAMICS remains **HYPOTHESIS**; S0/SM bound (do not reject) a pooled static-denylist prior on this pool/window; no PRODUCT_CORE promotion and no EXPERIMENTAL upgrade from a single window ladder.

## 9. Treatment / policy liveness

This is a Physics estimation experiment with no SPIDER treatment arm, so the packet's treatment-liveness requirement is **NOT_APPLICABLE** (it is Product-scoped). The live contrast that matters is realized: the anchor-state transfer predictor is measured against `B_EXCHANGE`, `B_CONSTANT_USABLE` and `B_MARGINAL`. `POLICY_STATIC_DENYLIST` is a bounded deterministic function of `ambient_class` (`DENY` if `ambient_class in barrier_set` else `ALLOW`) with a deterministic re-probe at `DENYLIST_HORIZON`; `POLICY_CLASS_CONDITIONAL_DENYLIST` is defined whenever SM is reached (long horizon for intrinsic classes, transient half-life for the rate class). Both return a defined decision for every class and terminate.

## 10. Validity threats (disclosed)

1. **Single network vantage.** The mandate's source-vantage axis is not varied; results are one egress. Explicit scope boundary against over-generalization.
2. **Window censoring.** The horizon is censored at `delta_ref = 1800 s`; timescales beyond 30 minutes are not measured.
3. **Weak-effect underpowering.** At N=57 the MI test has power ≈ 0.49–0.67 for `MI = delta_SKILL`; weak-but-real persistence is not reliably distinguishable from exchangeability. This is disclosed, and the design consequence is that `S0` requires positive change evidence and an ambiguous negative is `SIN`, never `S0`.
4. **Self-induced 429.** Single ambient GETs may still accumulate barriers; `C_PROBE_LOAD` measures the trend, `stratum_stress` isolates induced load, and the 52 unstressed endpoints plus `STATIONARITY_SKILL_NO_STRESS` are the clean persistence substrate.
5. **Coarse FA resolution.** The smallest non-zero FA is `1/n_denylisted` (≈0.11–0.17); `tau_FA = 0.10` therefore flags the pooled-denylist horizon as failed on **any** recovery. This is conservative and is why the pooled horizon is a reported product quantity while the primary stationarity/intrinsic-persistence decision is decoupled from it.
6. **Coarse intrinsic-persistence resolution.** `CLASS_PERSISTENCE` has resolution `1/n_intrinsic`; with `n_intrinsic ≈ 5` the ≥ 0.90 threshold requires ALL 5 to persist (4/5 = 0.80 fails). The intrinsic test is deliberately stringent; one flaky intrinsic endpoint routes S1/SM to S0 or SIN.
7. **Permutation vs. clustering.** The `B_EXCHANGE` null uses a global label shuffle (exchangeable endpoints) and does not preserve registrable-domain clusters; cluster dependence is addressed only by the bootstrap CI. This is a design choice, disclosed.
8. **Single-sample ambient state.** The ambient class is defined operationally by one GET per sweep (the honest input to a single-probe denylist), so stochastic within-endpoint rate noise can read as an ambient onset/recovery. The load probe and `AMBIENT_RECOVERY_n`/`AMBIENT_ONSET_n` expose this, and the class-conditional structure is what separates intrinsic persistence from rate noise.
9. **Pool composition.** Persistent 403-challenge endpoints dominate the pooled MI and can mask rate-driven non-stationarity; the class-conditional metrics and `STATIONARITY_SKILL_MULTI` guard against dilution.
10. **Live oracles** depend on third-party hosts (with a redundant 429 host); oracle failure is a measurement-invalid signal, not a negative.
11. **`/tmp` provenance.** Pre-freeze census/calibration/power/branch-probe artifacts are not persisted in the repo and are not interpretation dependencies; EXECUTE must re-derive all floors and calibrations from its own collected data (AUDIT should treat the census summary here as explanatory, not as frozen evidence).
12. **Pre-freeze census is outcome-adjacent pilot.** The 30 s window-pair census observes the same barrier/recovery/onset phenomenon on a subset of the same endpoints with the same classifier. Endpoints are parent-inherited (not census-selected), it is sanctioned as the mandate's attainability certificate, and it is not the frozen 5-sweep/1800 s measurement; AUDIT should note it as a pilot, not a confirmation.

## 11. Product consequences

- **S1_STATIONARY:** a static endpoint denylist is valid through ≥ 1800 s on this pool; adopt terminal classification with the measured `DENYLIST_HORIZON` as the re-probe interval; no online per-endpoint history model is needed for access decisions.
- **SM_CLASS_CONDITIONAL:** split the dead-end policy into an intrinsic-block track with a long horizon and a rate-driven track driven by `TRANSIENT_RECOVERY_HALF_LIFE` / `STRESS_FALSE_ACCEPT` (`POLICY_CLASS_CONDITIONAL_DENYLIST`); a pooled static denylist is unsafe.
- **S0_NON_STATIONARY:** endpoint access state changed within the ladder; re-observe before each use; no cached static per-endpoint access decision.
- **SIN_INCONCLUSIVE:** no policy change is licensed; the pooled-denylist horizon remains unmeasured on this pool/window.

## 12. Provenance / code binding

No mutable local fixture, task bank, dataset or pre-existing code file is an interpretation dependency; therefore `freeze_artifacts` is empty and `freeze_artifacts_bound` is `NOT_APPLICABLE`. All interpretation-determining constants (universe, `CHALLENGE_RE_LITERAL`, classifier and severity ranks, sweep ladder and the no-snapping partial-ladder rule, ambient/load probe definitions, strata, `registrable_domain` rule, thresholds, seeds, branch logic) are embedded verbatim in `spec.json` and this file, which the deterministic freezer hashes (`freeze.json.hashes.spec.json`, `prereg.md`). EXECUTE must implement the collection/analysis code strictly as a literal realization of these literals, must not introduce or retune any decision-relevant constant, and must record the code hash in `provenance.json` for AUDIT.

## 13. Non-duplication statement (pre-2.0 and pre-2.1)

`LEGACY: DISTINCT_EXTENSION` (Director mandate, confirmed by targeted primary-source reads).

The pre-2.0 `frontier/web-physics-volatility-freshness` program (closure artifact sha `3bc393fc8d3c5fc2515da6e8c7481b2618fefdbe`, `frontier/web-physics-volatility-freshness/reports/charters/v3/CLOSURE_REPORT.md`; prereg sha `f4cf72f72a07033608dda5a68c99cd6e13e07fd8`, `.../prereg/PREREG_STAGE0R_v1.md`; archive blob `9bb76113aeaf46d9aecdd8a38349a3a7741e57c3`) studied **content volatility/freshness over time windows** and closed as `PAUSE_CLOSE_NEGATIVE` on a structural data-insufficiency (max eligible span 0.0736 days < 7-day threshold). It measured whether page *content* changes, not whether an endpoint's *access-barrier class* persists. No located artifact measures access-barrier half-life, class-conditional persistence or a denylist false-accept horizon. The old physics `WP-003` (sha `292e3243d9bc7a3b88712788a7cb05709eb74eb9`) is `MEASUREMENT_INVALID` (target leakage) and `WP-003B` (sha `f6cfdfc749cae9eb4d9fcc4b11b94b63a2bcfb6e`) is a bounded mechanics result (action-only MSE 0.756 vs full 0.735), neither measuring access-state stationarity.

Within Research 2.0, `EXP-PHYSICS-37992957068` measured **next-request** barrier classification on a **single** window and bounded that sub-thread (`INCONCLUSIVE`; endpoint identity dominant; `AMBIENT_ONSET_n=0`). This experiment changes the object (endpoint access-state **persistence across a window ladder**), the falsifier direction (positive change vs stationarity), the deliverable (a class-conditional validity horizon / re-probe interval) and the branch structure (positive-change `S0`, decoupled from the coarse pooled-denylist horizon and from MI non-significance). It does **not** re-run next-request classification, value derivation/PMI, Graph `C-FRESHNESS` (content staleness) or Runtime `C-MEAS-VALID` drift controls.
