# EXP-PHYSICS-38074818597 — Preregistration (frozen before execution)

Lane: **physics**. Target claim: **C-WEB-DYNAMICS**. Director mandate action: **REOPEN**, cognitive reset, `parent_handoff_disposition` **USE**. `design_contract_version = 2`.

`spec.json` is the machine-binding source; where wording differs, `spec.json` governs. Do not edit after `freeze.json` exists.

## 1. What is tested

On the frozen 57-endpoint credential-free HTTP GET universe (inherited verbatim from `EXP-PHYSICS-37992957068`; **not extended**, because the pre-freeze attainability certificate is satisfied inside the frozen 57) we measure the **persistence/timescale of each endpoint's ambient ACCESS-BARRIER state** across a ladder of separated observation windows, and the **validity horizon of a static endpoint-level denylist**.

This changes the unit of study from *next-request* barrier classification (bounded by `EXP-PHYSICS-37992957068`) to *endpoint access-state persistence across windows*. It is orthogonal to the exhausted next-request / value-derivation / PMI sub-threads, to Graph `C-FRESHNESS` (staleness of inherited *content*) and to Runtime `C-MEAS-VALID` drift controls. The temporal/window axis is measured; the mandate's **source-vantage** axis is **not** varied and is a declared scope boundary (one stdlib-HTTP egress).

### 1.1 Branch design

The primary stationarity decision is made on **endpoint-identity information** (`STATIONARITY_SKILL`) and intrinsic-class persistence, **not** on the coarse pooled-denylist horizon (whose false-accept resolution is `1/n_denylisted = 1/6 ≈ 0.17` here, so a single rate-driven recovery would force `DENYLIST_HORIZON=0`). `S0_NON_STATIONARY` is defined by **positive change evidence**, not by a non-significant MI test; a non-significant MI with no change evidence is `SIN_INCONCLUSIVE`, never `S0`.

Frozen dispositions (both scientific directions reachable; `MEASUREMENT_INVALID` reserved exclusively for prerequisite/control failure):

- **S1_STATIONARY**: `STAT_SIG_SIGONLY` AND `INTRINSIC_PERSISTENT` AND `NOT RATE_TRANSIENT` AND `NOT STATE_CHANGE_EVIDENCE`.
- **S0_NON_STATIONARY**: `INTRINSIC_BREAK` OR (`STATE_CHANGE_EVIDENCE` AND no intrinsic class at T0).
- **SM_CLASS_CONDITIONAL**: `INTRINSIC_PERSISTENT` AND `RATE_TRANSIENT`.
- **SIN_INCONCLUSIVE**: otherwise (including a non-significant `STAT_SIG_SIGONLY` with no positive change evidence).

## 2. Frozen intrinsic classifier (response-intrinsic, no history leakage)

Each response is classified from its own stored fields only (status, `cf-mitigated`, first 262144 body bytes, error string). The classifier is bound to `research/physics/exp_37992957068_lib.py` (sha256 `767e2c56fc0fb79bb953f5f11d1223a4b82305782457eb346a70f94d41e1054f`); its regex is transcribed verbatim:

```
CHALLENGE_RE_LITERAL = (?i)(just a moment|cf-browser-verification|cf[-_]chl[-_]|challenge-platform|cf-challenge|cdn-cgi/challenge|attention required|checking your browser|enable javascript and cookies|verify you are human|please complete the security check|g-recaptcha|hcaptcha|recaptcha|cf-turnstile|<title>\s*just a moment)
```

| class | rule |
|---|---|
| `CLEAN` | status in {200,202} and body does not match `CHALLENGE_RE` |
| `RATE_LIMIT_429` | status == 429 |
| `BLOCK_403_CHALLENGE` | status == 403 and (`lower(cf-mitigated) == "challenge"` **or** body matches `CHALLENGE_RE`) |
| `UNAVAILABLE_403` | status == 403 without any challenge marker |
| `TRANSPORT_ERROR` | no HTTP response (DNS/connect/TLS/timeout) |
| `OTHER_NONBARRIER` | any other status (404, 500, redirect-to-error) **or** a 2xx carrying a challenge marker |

`barrier_set = {RATE_LIMIT_429, BLOCK_403_CHALLENGE, TRANSPORT_ERROR}`; `ordinary_unavailability_set = {UNAVAILABLE_403, OTHER_NONBARRIER}`; intrinsic classes = `{BLOCK_403_CHALLENGE, TRANSPORT_ERROR}`. Severity rank: `TRANSPORT_ERROR 5 > RATE_LIMIT_429 4 > BLOCK_403_CHALLENGE 3 > UNAVAILABLE_403 2 > OTHER_NONBARRIER 1 > CLEAN 0`. Classes depend only on a single request, so conditioning on the anchor state is not label leakage.

## 3. Frozen sweep protocol and strata

**Unit**: `(endpoint, sweep_index)`; anchor = sweep 0.

**Ladder** (target offsets, seconds): `[0, 30, 180, 720, 1800]`; `delta_ladder = [30, 180, 720, 1800]`; `delta_ref` = final sweep (nominal 1800). Analysis labels each sweep by its **nominal rung**; the final sweep's **actual** delta must be ≥ 1500 s or the run is `MEASUREMENT_INVALID`.

**Request policy**: GET only, follow ≤ 5 redirects, 30 s timeout, TLS verification on, **no retries, one attempt per observation** (so a DNS/connect/TLS/timeout failure is directly `TRANSPORT_ERROR`, not a retried `CLEAN`). Frozen User-Agent `SPIDER-research2/1.0 (+credential-free access-state persistence probe)`, `Accept: */*`. No authentication, JavaScript or credentials. Python 3.12 **stdlib only** (numpy is not required; the bound parent lib is hashed but not imported).

**Ambient probe (primary state)** — for EVERY endpoint: a fresh cookie jar, then exactly **one** GET. `ambient_class` = classifier output. Endpoints are probed sequentially in a per-sweep frozen seeded permutation (seed `38074818597`), inter-endpoint gap 0.30 s.

**Load probe (transient-class diagnostic only)** — immediately after its ambient probe, each `stratum_stress` endpoint receives a burst of `B_stress = 8` GETs at 0.15 s in a **separate** fresh cookie jar; `load_class` = argmax severity rank. The other 52 endpoints get no load probe.

**Primary state for all stationarity/denylist metrics is `ambient_class`.**

**`stratum_stress`** (fixed, NOT outcome-selected): `https://www.djangoproject.com/admin/login/`, `https://www.djangoproject.com/accounts/login/`, `https://auth0.com/`, `https://search.brave.com/search?q=test`, `https://community.home-assistant.io/`.
**`stratum_intrinsic_candidates`** (fixed): `https://gitlab.com/users/sign_in`, `https://community.cloudflare.com/`, `https://www.npmjs.com/login`, `https://wordpress.com/log-in`, `https://www.phpbb.com/community/`, `https://community.invisioncommunity.com/`.

## 4. Metrics, baselines and stable identifiers

- `STATIONARITY_SKILL` (**primary**) = plug-in binary mutual information `I(B_anchor; B_delta)` over the ambient barrier indicator, in nats/endpoint, at `delta_ref`; `B_EXCHANGE` global endpoint-permutation p-value (10000 uniform shuffles of the lag vector; seed 38074818597); endpoint-clustered bootstrap 95% CI (cluster = `registrable_domain`, 10000 resamples, seed 38074818597). `STATIONARITY_SKILL_BY_LAG` reports each rung; `STATIONARITY_SKILL_NO_STRESS` repeats the primary at `delta_ref` on the 52 non-stressed endpoints. `STATIONARITY_SKILL_MULTI` = 6-class MI.
- `registrable_domain(url)` (frozen): URL host, strip one leading `www.`, retain the final two dot-separated labels (no multi-label public suffix occurs in the frozen 57), e.g. `gitlab.gnome.org → gnome.org`.
- `DENYLIST_FALSE_ACCEPT(delta)` = fraction of T0 ambient-barrier endpoints non-barrier at `delta`; `DENYLIST_FALSE_REJECT(delta)` = fraction of T0 ambient-nonbarrier endpoints barrier at `delta`.
- `DENYLIST_HORIZON` = largest ladder delta such that FA and FR pass (≤ 0.10) at **every** lag up to and including it (contiguous prefix), else 0; `DENYLIST_FIRST_FAIL_LAG` = smallest failing delta, else null.
- `CLASS_PERSISTENCE` (per class) = fraction of endpoints with that T0 ambient class whose `delta_ref` ambient class is identical.
- `INTRINSIC_PERSISTENT` = ≥ 1 intrinsic class present at T0 AND every present intrinsic class has `CLASS_PERSISTENCE ≥ 0.90`; `INTRINSIC_BREAK` = intrinsic present at T0 AND NOT `INTRINSIC_PERSISTENT`.
- `RATE_TRANSIENT` = `(STRESS_FALSE_ACCEPT > 0.10)` OR `(median TRANSIENT_RECOVERY_HALF_LIFE finite and < 1800)` OR `(a RATE_LIMIT_429 endpoint is present at T0 and CLASS_PERSISTENCE[RATE_LIMIT_429] < 0.90)` OR `(AMBIENT_RECOVERY_n > 0)` OR `(STRESS_ONSET_n > 0)`.
- `STATE_CHANGE_EVIDENCE` = `(AMBIENT_RECOVERY_n > 0)` OR `(AMBIENT_ONSET_n > 0)` OR `(DENYLIST_FALSE_ACCEPT(1800) > 0.10)` OR `(DENYLIST_FALSE_REJECT(1800) > 0.10)`.
- `TRANSIENT_RECOVERY_HALF_LIFE`, `STRESS_FALSE_ACCEPT`, `C_PROBE_LOAD`, `AMBIENT_ONSET_n`, `AMBIENT_RECOVERY_n`, `STRESS_ONSET_n`, `PERSIST_n`, `DENYLIST_SKILL`, power diagnostics as in `spec.json`.

Baselines: `B_EXCHANGE` (global lag-label permutation null), `B_CONSTANT_USABLE` (always-usable floor), `B_MARGINAL`, `B_LASTSWEEP`. Stable ids: metric `STATIONARITY_SKILL`; controls `PC_SYNTHETIC_STATIONARY, PC_ORACLE_BARRIER, NC_SYNTHETIC_EXCHANGEABLE, NC_CLEAN_ORACLE, C_PROBE_LOAD`; policies `POLICY_STATIC_DENYLIST, POLICY_CLASS_CONDITIONAL_DENYLIST`; branches `S1_STATIONARY, S0_NON_STATIONARY, SM_CLASS_CONDITIONAL, SIN_INCONCLUSIVE, MEASUREMENT_INVALID`. Seeds: probe_order/bootstrap/permutation/pc = 38074818597; nc = 38074818598.

## 5. Null calibration (pre-freeze, non-outcome-bearing)

The mandated memory/constant null is `B_EXCHANGE`: a global uniform shuffle of the lag barrier labels across all endpoints (anchor marginals preserved), recomputing `I(B_anchor;B_delta)` — i.e. the identity-transfer predictor is no better than the constant-marginal predictor. Fresh calibration ran the **actual** estimator on synthetic data (no Web data; `probe_offline.py` sha256 `9868930f8d8fde2375dab1a534d0798219f8ef711dae617dd7b76eedc85dabb4`; raw output sha256 `2edde402348a8334f700a06c4653219ffabf0b403a1c56ac6282f55961680268`):

| control | configuration | frozen bound | fresh achieved |
|---|---|---|---|
| `NC_SYNTHETIC_EXCHANGEABLE` | independent anchor/lag, p=0.20 | FP ≤ 0.05 | **0.01** |
| `NC_SYNTHETIC_EXCHANGEABLE` | independent anchor/lag, p=0.30 | FP ≤ 0.05 | **0.03** |
| `PC_SYNTHETIC_STATIONARY` | f_b=0.20, rho=0.80 | power ≥ 0.80 | **1.00** |
| `PC_SYNTHETIC_STATIONARY` | f_b=0.10, rho=0.80 | power ≥ 0.80 | **0.95** |
| `PC_SYNTHETIC_STATIONARY` | f_b=0.10, rho=0.50 (disclosed corner) | (informational) | 0.74 |

Minimum-meaningful-effect power (N=57, R=150, 1000 perms): a generator whose true MI equals `delta_SKILL = 0.05` nats has power **0.61** at `f_b=0.105` (rho*=0.387), 0.59 at 0.10, 0.61 at 0.20, 0.56 at 0.30.

**Frozen consequence:** at this n a *weak-but-real* persistence (`MI ≈ 0.05`) is only ~0.6-powered, while strong persistence (`rho ≈ 0.8–1.0`) is fully powered. Therefore absence of significance cannot be used to claim non-stationarity; `S0` requires positive change evidence and an ambiguous negative is `SIN`. This calibrates the estimator and null; it does not assert any real endpoint is stationary.

## 6. Attainability certificate (pre-freeze, non-outcome-bearing)

All pre-freeze activity is non-confirmatory and establishes reachability + calibration only. Scripts are under `/tmp/opencode/phys380_cal/` and are **not** frozen interpretation dependencies; EXECUTE re-verifies every floor from its own data.

### 6.1 Window-pair census (`probe_live.py` sha256 `ce8b7254da6ce35cd18a8a67d7a18fe7209ec30ca0af4acf801633612593fa6e`; raw sha256 `5ad98c83a1e72b73e9f193eef8f245abda1192ef9bbc95a2416b60e99a777408`)

Full frozen 57, two cold-GET sweeps ≈ 160 s apart, plus a 6-GET burst on the 5 rate-capable endpoints. Observed window-A histogram `{BLOCK_403_CHALLENGE: 5, TRANSPORT_ERROR: 1, OTHER_NONBARRIER: 5, CLEAN: 46}`; **6 stably persistent barriers** across the pair: `gitlab.com/users/sign_in`, `community.cloudflare.com`, `www.npmjs.com/login`, `wordpress.com/log-in`, `www.phpbb.com/community/` (all `BLOCK_403_CHALLENGE`) and `community.invisioncommunity.com` (`TRANSPORT_ERROR`, a DNS-unresolvable host from this egress). No ambient recovery/onset was observed in this particular pair.

### 6.2 Recovery and newly-blocking reachability

Induce-then-cold-probe on `https://www.djangoproject.com/accounts/login/`: a 8-GET burst produced `RATE_LIMIT_429` (positions 7–8), and a cold GET at +10 s and again at +30 s both returned `CLEAN`. So a **newly-blocking** endpoint is reachable under load and a rate-driven barrier **recovers** under ambient re-observation within the tested scale. Parent accepted evidence independently recorded 13 RECOVERY events and rate-limit onsets on the same stratum.

### 6.3 Branch reachability through the actual metric (`probe_offline.py`)

| synthetic world | result |
|---|---|
| stationary (6 persistent challenge + 51 clean) | MI 0.3365, intrinsic persistent, no rate transient, no change → **S1** |
| exchangeable/positive-change (≥3 T0 barriers) | `INTRINSIC_BREAK` true, FA 0.25 → **S0** |
| class-conditional (6 persistent + 3 recovering rate) | intrinsic persistent + `RATE_TRANSIENT`, FA 0.333 → **SM** |
| intrinsic-persistent + one new non-rate block | `STATE_CHANGE` true, `INTRINSIC_BREAK` false, `RATE_TRANSIENT` false → **SIN** |

`MEASUREMENT_INVALID` is produced only by prerequisite/control failure, never by a scientific outcome.

### 6.4 Arithmetic floors

- T0 ambient-barrier endpoints ≥ **6** (5 persistent 403-challenge + 1 persistent transport) ⇒ hard floor ≥ 3 satisfied; T0 intrinsic endpoints ≥ **6** (certified reachable, a reported floor rather than a hard gate).
- `f_b_obs ≈ 6/57 = 0.105`.
- `S1`, `S0`, `SM`, `SIN` all reachable (6.3); `FA > 0.10` reachable (any recovery with `n_denylisted ≥ 3` gives FA ≥ 0.33); `FR > 0` reachable via the demonstrated load-induced onset.

**Certificate verdict: SATISFIED.** Both persistently-blocked and recovering/newly-blocking endpoints are reachable across the window pair, so the experiment proceeds rather than parking. If EXECUTE cannot re-verify the floors the packet is `MEASUREMENT_INVALID`, the operational analogue of PARK.

## 7. Controls

- `PC_SYNTHETIC_STATIONARY` (offline, f_b=0.20, rho=0.80, R=200, seed 38074818597): power ≥ 0.80 required, fresh 1.00.
- `NC_SYNTHETIC_EXCHANGEABLE` (offline, p=0.20, R=200, seed 38074818598): false-positive ≤ 0.05 required, fresh 0.01.
- `PC_ORACLE_BARRIER` (live): httpbin 429 and httpbingo 429 → `RATE_LIMIT_429`; no-such-host.invalid → `TRANSPORT_ERROR`; httpbin 403 → `UNAVAILABLE_403`.
- `NC_CLEAN_ORACLE` (live): httpbin 200/uuid and example.com → `CLEAN`.
- `C_PROBE_LOAD` (validity control): Cochran-Armitage trend of ambient barrier prevalence across sweeps for the 52 non-stress endpoints, plus the `STATIONARITY_SKILL_NO_STRESS` replica.
- Classifier replay must yield 0 mismatches re-deriving every class from stored fields.

Any control failure / unreachable network (including BOTH 429 oracles challenged) / non-reproducible classifier / T0 floors unmet / delta_ref actual < 1500 s ⇒ `status = MEASUREMENT_INVALID`.

## 8. Decision rule

Thresholds: `tau_FA = tau_FR = 0.10`, `alpha = 0.05`, `delta_SKILL = 0.05` nats, PC power ≥ 0.80, NC FP ≤ 0.05, intrinsic persistence ≥ 0.90, T0 barrier floor ≥ 3 (intrinsic presence certified at ≥ 6 but not gated), 10000 permutations/resamples. Gates and branch precedence are frozen in `spec.json.decision_rule`:

1. `MEASUREMENT_INVALID` (prerequisite/control failure only).
2. `S0_NON_STATIONARY` if `INTRINSIC_BREAK` OR (`STATE_CHANGE_EVIDENCE` AND no intrinsic class at T0) — positive change evidence.
3. `S1_STATIONARY` if `STAT_SIG_SIGONLY AND INTRINSIC_PERSISTENT AND NOT RATE_TRANSIENT AND NOT STATE_CHANGE_EVIDENCE`.
4. `SM_CLASS_CONDITIONAL` if `INTRINSIC_PERSISTENT AND RATE_TRANSIENT`.
5. `SIN_INCONCLUSIVE` otherwise.

Power diagnostics (`MI_POWER_OK`, `POWER_AT_RHO90`, `POWER_AT_DELTA_SKILL`) are reported, not gating. Claim ceiling: C-WEB-DYNAMICS remains **HYPOTHESIS**; no PRODUCT_CORE promotion and no EXPERIMENTAL upgrade from this single window ladder.

## 9. Treatment / policy liveness

Physics estimation experiment, no SPIDER treatment arm ⇒ `treatment_liveness = NOT_APPLICABLE` (Product-scoped). `POLICY_STATIC_DENYLIST` is a bounded deterministic function of `ambient_class` (`DENY` if in `barrier_set` else `ALLOW`) with a re-probe at `DENYLIST_HORIZON`; `POLICY_CLASS_CONDITIONAL_DENYLIST` is defined whenever SM is reached. Both terminate for every class.

## 10. Validity threats (disclosed)

1. **Single network vantage** — mandate's source-vantage axis not varied; one egress. Declared scope boundary.
2. **Window censoring** — horizon censored at `delta_ref = 1800 s`.
3. **Weak-effect underpowering** — MI power ≈ 0.6 for `MI = 0.05`; hence `S0` requires positive change evidence and an ambiguous negative is `SIN`.
4. **Self-induced 429** — `C_PROBE_LOAD` and the 52 unstressed endpoints isolate induced load.
5. **Coarse FA resolution** — smallest non-zero FA is `1/n_denylisted`; `tau_FA = 0.10` flags the pooled horizon on any recovery, which is why the horizon is a reported product quantity decoupled from the primary branch.
6. **Coarse intrinsic-persistence resolution** — with `n_intrinsic ≈ 6`, `CLASS_PERSISTENCE ≥ 0.90` requires all 6 to persist; one flaky intrinsic endpoint routes S1/SM to S0/SIN.
7. **Permutation vs. clustering** — the global shuffle does not preserve registrable-domain clusters; clustering is addressed by the bootstrap CI.
8. **Single-sample ambient state** — the ambient class is one GET per sweep; stochastic rate noise can read as an onset/recovery, which the load probe and `AMBIENT_*` counters expose.
9. **`/tmp` provenance** — pre-freeze census/calibration scripts are not in the repo and are not interpretation dependencies; EXECUTE re-derives all floors and calibrations.
10. **Pre-freeze census is outcome-adjacent pilot** — it observes the same phenomenon on the same endpoints; endpoints are parent-inherited (not census-selected), it is the sanctioned attainability certificate, and it is not the frozen 5-sweep/1800 s measurement. AUDIT should note it as a pilot, not a confirmation.

## 11. Product consequences

- **S1_STATIONARY:** static denylist valid ≥ 1800 s on this pool; adopt terminal classification with the measured `DENYLIST_HORIZON` as the re-probe interval.
- **SM_CLASS_CONDITIONAL:** split the policy into an intrinsic-block track with a long horizon and a rate-driven track driven by `TRANSIENT_RECOVERY_HALF_LIFE`/`STRESS_FALSE_ACCEPT` (`POLICY_CLASS_CONDITIONAL_DENYLIST`); a pooled static denylist is unsafe.
- **S0_NON_STATIONARY:** re-observe before each use; no cached static per-endpoint access decision.
- **SIN_INCONCLUSIVE:** no policy change licensed; horizon remains unmeasured on this pool/window.

## 12. Provenance / code binding

`freeze_artifacts = ["research/experiments/EXP-PHYSICS-37992957068/spec.json", "research/physics/exp_37992957068_lib.py"]`; `freeze_artifacts_bound = PASS`. Both are existing mutable repository files whose identity can change the interpretation: the parent `spec.json` (sha256 `38ec8d15fac9b7e50fda5825c130a409d4211a341076023b9112548ccd3fa2d2`) defines the inherited 57-endpoint universe and class partition, and the parent `lib.py` (sha256 `767e2c56fc0fb79bb953f5f11d1223a4b82305782457eb346a70f94d41e1054f`) is the classifier source of record. The deterministic freezer hashes them into `freeze.json.artifact_hashes`. Every other interpretation-determining constant is embedded verbatim in `spec.json`/prereg.md, which the freezer also hashes. EXECUTE must implement the collection/analysis code strictly as a literal realization of those embedded constants (no retuning), record its hash in `provenance.json`, and must not import the bound parent lib (numpy is not a dependency).

## 13. Non-duplication statement (pre-2.0)

`LEGACY: DISTINCT_EXTENSION` (Director mandate, confirmed by targeted primary-source reads). The pre-2.0 `frontier/web-physics-volatility-freshness` program (sha `3bc393fc8d3c5fc2515da6e8c7481b2618fefdbe`; prereg sha `f4cf72f72a07033608dda5a68c99cd6e13e07fd8`; blob `9bb76113aeaf46d9aecdd8a38349a3a7741e57c3`) studied **content volatility/freshness over time windows** and closed `PAUSE_CLOSE_NEGATIVE` on structural data-insufficiency; it did not measure access-barrier class persistence or a denylist false-accept horizon. `P2-WP003` (sha `292e3243d9bc7a3b88712788a7cb05709eb74eb9`) is `MEASUREMENT_INVALID`; `P2-WP003B` (sha `f6cfdfc749cae9eb4d9fcc4b11b94b63a2bcfb6e`) is a bounded mechanics result; neither measures access-state stationarity. Within Research 2.0, `EXP-PHYSICS-37992957068` measured **next-request** barrier classification in a **single** window and bounded that sub-thread. This experiment changes the object (endpoint state persistence across a window ladder), the falsifier direction (positive change vs stationarity), the deliverable (a class-conditional validity horizon / re-probe interval) and the branch structure, and does not re-run next-request classification, value derivation/PMI, Graph `C-FRESHNESS` or Runtime `C-MEAS-VALID` drift controls.
