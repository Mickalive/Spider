# EXP-PHYSICS-37992957068 — Preregistration (frozen before execution)

Lane: **physics**. Target claim: **C-WEB-DYNAMICS**. Director mandate action: **PIVOT**, cognitive reset, parent_handoff_disposition **USE**.

This document is frozen together with `spec.json`; `spec.json` is the machine-binding source. Where wording differs, `spec.json` governs. Do not edit after `freeze.json` exists.

## 1. What is tested

On the frozen 57-endpoint credential-free universe inherited verbatim from EXP-PHYSICS-37973239386, we test whether **access barriers** — `RATE_LIMIT_429`, `BLOCK_403_CHALLENGE`, `TRANSPORT_ERROR` — have ONSET/RECOVERY dynamics predictable from **observable request history** (recent request rate, burstiness, inter-request spacing, cookie-jar freshness, within-session barrier history) *beyond* endpoint identity and persistence-memory, whether barriers are separable from ordinary unavailability (`UNAVAILABLE_403`, `OTHER_NONBARRIER` = 404/500), and whether an **adaptive scheduler** (`A_ADAPT`) can hold per-endpoint success near its no-barrier baseline with **strictly fewer requests** than the **unconditional retry** baseline (`A_RETRY`).

Two scientific outcomes are frozen and both are reachable:

- **S1_SUPPORTS**: SKILL_LL >= 0.05 nats with endpoint-clustered CI lower > 0, AND A_ADAPT uses strictly fewer mean requests than A_RETRY on the barrier-exposed stratum at non-inferior success.
- **S0_FALSIFIES**: SKILL_LL <= 0 with CI upper < 0.05, no transition class positive, AND d_Req >= 0. Under S0 the barrier sub-thread of C-WEB-DYNAMICS is *bounded* on this pool/window (not closed).

`MEASUREMENT_INVALID` is reserved exclusively for prerequisite/control failure and must never be reported as a scientific negative.

## 2. Frozen intrinsic classifier (response-intrinsic, no history leakage)

Each response is classified from its own stored fields only:

| class | rule |
|---|---|
| `CLEAN` | HTTP 2xx (200/202) and body has no challenge marker |
| `RATE_LIMIT_429` | HTTP 429 |
| `BLOCK_403_CHALLENGE` | HTTP 403 and (`cf-mitigated: challenge` **or** body matches the frozen Cloudflare "Just a moment"/captcha marker regex) |
| `UNAVAILABLE_403` | HTTP 403 without any challenge marker |
| `TRANSPORT_ERROR` | no HTTP response (DNS/connect/TLS/timeout) |
| `OTHER_NONBARRIER` | any other HTTP status (404, 500, …) |

`barrier_set = {RATE_LIMIT_429, BLOCK_403_CHALLENGE, TRANSPORT_ERROR}`.
`ordinary_unavailability_set = {UNAVAILABLE_403, OTHER_NONBARRIER}`.
`ONSET event = (prev == CLEAN) and (cur in barrier_set)`. `RECOVERY event = (prev in barrier_set) and (cur == CLEAN)`.

Every request stores raw status, `server`, `cf-mitigated`, `retry-after`, body SHA-256, byte length, elapsed ms, and error string, so AUDIT recomputes the class deterministically. The in-session strings `discuss.python.org` vs `chat.python.org` are treated as distinct hosts; no aliasing.

## 3. Frozen arms and randomization

Arm definitions (identical to `spec.json.frozen_arm_design`):

- `A_RETRY` (REQUIRED no-adaptation / unconditional-retry baseline): same session, gap 0.5 s, up to J_max=5 requests, stop at first CLEAN; retries on any non-CLEAN class.
- `A_RETRY_SPACED` (no-adaptation rate baseline): same session, gap 4.0 s, J_max=5, stop at first CLEAN.
- `A_FRESH` (no-adaptation session-freshness baseline): fresh cookie jar before each request, gap 4.0 s, J_max=5, stop at first CLEAN.
- `A_ADAPT` (treatment): CLEAN→stop; `RATE_LIMIT_429`→honor `Retry-After` (cap 30 s) else wait 8.0 s, same session, retry; `BLOCK_403_CHALLENGE`→stop; `UNAVAILABLE_403`/`OTHER_NONBARRIER`→stop; `TRANSPORT_ERROR`→retry once after 3.0 s with a fresh jar, then stop. J_max=5.

12 sessions per endpoint; within each endpoint the 12 sessions are assigned 3 per arm by a seeded permutation (seed 37992957068). GET only, one frozen User-Agent, no credentials, no JavaScript.

## 4. Models, baselines and stable metric identities

- `M_HISTORY`: regularized logistic regression on {arm, j, gap, session_fresh, prev_label, n_barrier_so_far, time_since_last_barrier, endpoint_id}.
- `M_HISTORY_NOID`: endpoint-identity ablation of the same model.
- Nulls: `B_CONSTANT`, `B_ENDPOINT_CONST` (identity), `B_MEMORY_PERSIST` (memory), `B_RATE_ONLY` (schedule only). The primary metric is measured against the **maximum** over all four.
- `SKILL_LL` = held-out log-loss improvement (nats/request) of M_HISTORY over max(nulls); leave-one-session-out CV; endpoint-clustered bootstrap 95% CI (10000 resamples, seed 37992957068). `SKILL_BA` is balanced-accuracy analogue.
- Transition metrics: `ONSET_SKILL_LL`, `RECOVERY_SKILL_LL`. Separability: `SEPARABILITY_SKILL_LL` (barrier_set vs ordinary_unavailability_set).
- Scheduler metrics on the barrier-exposed stratum: `d_Req = mean_requests(A_ADAPT) − mean_requests(A_RETRY)`, `d_Succ`, `endpoint_no_barrier_success` (pooled first-request CLEAN fraction), `ADAPT_abs_requests`, `RETRY_abs_requests`.

## 5. Attainability certificate (pre-freeze, non-outcome-bearing)

A reachability census was run pre-freeze on 14 of the 57 frozen endpoints (all 14 are in the frozen universe), 2 fresh sessions each, J=6 GETs at gap 0.15 s, plus an 8 s recovery probe. Raw output: `/tmp/opencode/phys379/census.json`. It is **non-confirmatory** and only establishes that the required event classes are reachable in this environment; it is not part of the frozen design's measurements.

Observed over 168 planned GETs: 60 `BLOCK_403_CHALLENGE` (5 persistent endpoints), 16 `RATE_LIMIT_429`, 12 `TRANSPORT_ERROR` (1 persistent endpoint), 80 `CLEAN`. Within-session transitions observed live: 2 `ONSET` (djangoproject/admin `CLEAN→429`; auth0 `CLEAN→429`) and 2 `RECOVERY` (djangoproject/admin `429→CLEAN`). Recovery probes: djangoproject/admin returned CLEAN after 8 s (recoverable 429); auth0/brave remained 429; static 403 and the transport endpoint never recovered.

Arithmetic lower bound on barrier events in the frozen run, using **only** persistent endpoints guaranteed by the census (no transient assumptions):

- 5 persistent `BLOCK_403_CHALLENGE` endpoints: A_RETRY/A_RETRY_SPACED/A_FRESH contribute 3×5=15 each, A_ADAPT contributes 3×1=3 → 48 per endpoint → **240**.
- 1 persistent `TRANSPORT_ERROR` endpoint: 3×5×3 + 3×2 = 45+6 → **51**.
- 1 persistent `RATE_LIMIT_429` endpoint (search.brave): 45 + 3×5=15 → **60**.

Lower bound = **351 barrier events** from guaranteed endpoints alone, ≫ the 30-event scheduler floor and ≫ the 3-endpoint barrier-exposed floor. Therefore the scheduler stratum and the primary pooled next-request task are reachable regardless of transient behavior. `ONSET`/`RECOVERY` are demonstrated reachable (2 each) but their count is **not** guaranteed by constant bars; hence transition metrics are **secondary/diagnostic only**, and the primary `PRED_PASS`/`PRED_FAIL` branch depends only on the pooled next-request task with hundreds of guaranteed barrier events. This closes the "unreachable/empty branch" attack: both S0 and S1 are arithmetically attainable, and neither transition behaviour nor a lucky transient endpoint is required for the primary branch to be evaluable.

A second design-time probe checked baseline identifiability directly through the frozen metric (no Web data, non-confirmatory; script `/tmp/opencode/phys379/probe_baseline_identifiability.py`). The same leave-one-endpoint-out logistic comparison gave SKILL_LL = **-0.079** (all 6 seeds <= 0) on a memoryless endpoint-constant plant — the endpoint-constant null sits at the achievable ceiling and history adds nothing — and SKILL_LL = **+0.077** (5/6 seeds > 0) on a schedule-dependent plant. This confirms that `PRED_FAIL` (S0) and `PRED_PASS` (S1) are both reachable through the actual metric, not just in principle; the real `PC_SYNTHETIC_DYNAMICS`/`NC_SYNTHETIC_MEMORYLESS` controls use R=200 with a larger planted effect to certify the >= 0.80 / <= 0.05 bounds.

## 6. Controls

- `PC_SYNTHETIC_DYNAMICS` (offline planted hazard, R=200, seed 37992957068): power to recover a schedule-dependent effect must be >= 0.80.
- `NC_SYNTHETIC_MEMORYLESS` (offline i.i.d. endpoint-constant barriers, R=200, seed 37992957069): false-positive rate <= 0.05.
- `PC_BARRIER_ORACLE` (live): `httpbin.org/status/403`, `httpbin.org/status/429`, and a guaranteed-unresolvable host must classify into the expected barrier classes.
- `NC_CLEAN_ORACLE` (live): `httpbin.org/status/200`, `httpbin.org/uuid` must classify CLEAN.

Any control failure / unreachable network / non-reproducible classifier / scheduler stratum below floors ⇒ `status = MEASUREMENT_INVALID`.

## 7. Decision rule

See `spec.json.decision_rule`. Thresholds: delta_SKILL = 0.05 nats, alpha = 0.05, margin_success = 0.05, PC power >= 0.80, NC FP <= 0.05. Branch precedence: MEASUREMENT_INVALID → S1_SUPPORTS → S0_FALSIFIES → S2_MIXED → INCONCLUSIVE. Claim ceiling for this sub-thread: at most C-WEB-DYNAMICS = EXPERIMENTAL; S0 bounds but does not reject the claim.

## 8. Treatment liveness

EXECUTE's first action is a **non-network** policy trace proving `A_ADAPT` returns a defined action for every intrinsic class and terminates within J_max=5 (recorded in provenance). This ensures the treatment is structurally executable before any collection; it is not a scientific measurement.

## 9. Validity threats (disclosed)

1. **Dominance of endpoint-constant barriers.** The pool is likely dominated by static behaviour; this is a genuine S0 risk, not a bug. The strong identity/persistence nulls are designed to capture exactly this, and S0 is a first-class result.
2. **Run-defined barrier-exposed stratum.** The scheduler stratum is defined by observed barriers; it is a pre-registered conditional subgroup, and the fixed pre-freeze candidate set (§ in `spec.json.scheduler_strata`) is additionally reported to guard against subgroup cherry-picking.
3. **Sequential policy selection.** For retry arms, later requests only occur after non-CLEAN responses; the CV respects time order and uses only past features, but the request population is policy-dependent. Disclosed; both nulls see the same population.
4. **Non-stationarity across windows.** The parent's djangoproject `/accounts/login` was 429-heavy while the census window was clean; rates are window-specific. The report must state this and not generalize to the Web.
5. **Self-induced 429.** Aggressive arms may induce 429s. That is precisely the rate mechanism under test (Q1/Q3); it is not a confound, and A_RETRY_SPACED/A_FRESH isolate gap and session-freshness effects.
6. **Live oracles** depend on third-party hosts; oracle failure is a measurement-invalid signal, not a negative.

## 10. Product consequences

- **Positive (S1):** adopt a mechanical prior — terminal dead-end classification for endpoint-constant barriers plus 429-aware backoff / fresh-session-on-transport scheduling that approaches no-barrier success with fewer requests than unconditional retry.
- **Negative (S0):** adopt a static per-endpoint dead-end denylist with immediate terminal classification and do **not** invest in an online barrier-history model; bound the barrier sub-thread of C-WEB-DYNAMICS on this pool/window.

## 11. Provenance / code binding

No mutable local fixture, task bank, dataset, or pre-existing code file is an interpretation dependency; therefore `freeze_artifacts` is empty and `freeze_artifacts_bound` is `NOT_APPLICABLE`. All interpretation-determining constants are embedded in `spec.json` and this file, which the freezer hashes. EXECUTE must implement the collection/analysis code strictly as a literal realization of these literals, must not introduce or retune any decision-relevant constant, and must record the code hash in `provenance.json` for AUDIT.
