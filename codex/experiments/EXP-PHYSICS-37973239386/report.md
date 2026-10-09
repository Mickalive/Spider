# EXP-PHYSICS-37973239386 — EXECUTE report

**Lane:** physics  
**Claim:** `C-WEB-DYNAMICS` (HYPOTHESIS)  
**Status:** `COMPLETE`  
**Outcome:** `FALSIFIES` (frozen branch S0)  
**Frozen input hashes verified:** `True`

## 1. Result in one paragraph

On a fresh confirmatory collection of the frozen 57-endpoint credential-free universe (1368 planned GETs, 24 transport errors = 1.75%, 0 non-GET, 0 credentialed), admission yielded 47 action-gating fields (46 PRIMARY SESSION/CSRF/TOKEN + 1 NONCE) across 27 registrable domains. Of 46 indicator fields, 2 were classified PREDICTABLE beyond `B_MEMORY_REPEAT` by >= `DELTA_MEM`=0.10, giving `PREDICTABLE_PREVALENCE_POOLED` = 0.0435 (site-clustered 95% CI [0.0000, 0.1163], 27 clusters, 10000 distinct resamples). Because PV <= P_FLOOR=0.10 **and** the clustered CI upper bound is < P_HI=0.25, the frozen precedence resolves to **S0 / FALSIFIES**: on this substrate class and window, server-minted action-gating values are observation-bound. No measurement-invalid condition (a)–(h) holds, so this is a valid scientific negative, not an instrument failure.

## 2. What was counted

The two PREDICTABLE fields:

- `pypi.org` — `cookie` `session_id`: rule(s) ['R_WALLCLOCK_B64'], detection fraction 1.00, `B_MEMORY_REPEAT` holdout 0.71, class `WALLCLOCK_B64`.
- `reddit.com` — `input.hidden` `jsc_token`: rule(s) ['R_CONST_SUBSTRING'], detection fraction 1.00, `B_MEMORY_REPEAT` holdout 0.00, class `CONST_SUBSTRING`.

Mechanism detail (evidence: `raw/collection.jsonl`, `derived/fields.json`):

- **pypi.org `session_id`** is a 3-segment dotted token; the middle segment is the byte-identical string `aslBhA` across all 8 session values and base64-decodes to `6ac94184`, whose big-endian 4-byte integer 1791574404 falls within the frozen +/-3600 s wall-clock window of the collection epoch. This is a genuine embedded epoch-like quantity (an itsdangerous-style timestamp region), not a chance match: the rule requires >= 0.75 of observations to independently hit, and a random 4-byte window lands in a 1-hour window with probability ~1.7e-6.
- **reddit.com `jsc_token`** values are 64 lowercase hex characters sharing a constant 32-hex-character prefix while remaining distinct; `R_CONST_SUBSTRING` therefore fires at fraction 1.0. This is a real constant structural shell, not an artifact.
- The other 44 indicator fields had no armed rule fire: persistent session cookies (`_gitlab_session`, `authSession`, `*_Session`, `flarum_session`, ...) are memory-repeat-explained (holdout ~0.71), and per-request CSRF/one-time tokens (`authenticity_token`, `wpLoginToken`, `csrfmiddlewaretoken`, `csrf-token`, `discourse-track-view-session-id`) vary without any rule firing.

## 3. Controls and baselines (EXECUTE re-run, separately from DESIGN literals)

| id | expected | observed | pass |
|----|----------|----------|------|
| `B_MEMORY_REPEAT` | near 0 for varying values | mean holdout 0.3362 | n/a (disqualifier baseline) |
| `B_MARKOV1` | sensitivity reference | mean 0.0590 | n/a |
| `B_CONSTANT_MODE` | 0 (constants excluded) | mean 0.0000 | n/a |
| `B_IRREDUCIBILITY_NULL` | aggregate FP <= 0.05 | EXECUTE 0.0000; DESIGN literal 0.000625 | True |
| `PC_PLANTED_CLASSES` | power >= 0.8 all classes | power_min 1.00 (8x200/200) | True |
| `NC_PLANTED_RANDOM_PLUS_LIVE` | planted FP <= 0.05 and live FP <= 0.05 | planted 0.0, live fired fraction 0.00 | True |

All 11 frozen non-baseline rules remain ARMED. `NON_GET_REQUESTS` = 0; `TRANSPORT_ERROR_RATE` = 0.0175 (<= 0.30). DESIGN-embedded literal null fired 1/1600 (FP 0.000625, `R_WALLCLOCK_B64`); the EXECUTE frozen-seed re-run fired 0/1600. Both satisfy FP <= 0.05; the discrepancy is disclosed (see `result.json` `validity_notes` V2, O11).

## 4. Measurement-validity conditions

- `(a) >= 20 indicator fields`: violated = `False`
- `(b) >= 8 registrable sites`: violated = `False`
- `(c) null pass`: violated = `False`
- `(d) PC power >= 0.8`: violated = `False`
- `(e) transport <= 0.30 and no non-GET`: violated = `False`
- `(f) locator/class coverage`: violated = `False`
- `(g) frozen universe verbatim`: violated = `False`
- `(h) frozen rule family`: violated = `False`

No condition is violated. `N_INDICATOR_FIELDS` = 46 (>= 20), `ADMITTED_SITES` = 27 (>= 8), universe used verbatim, rule family unchanged.

## 5. Branch precedence

```
1. MEASUREMENT_INVALID  -> not triggered (all (a)-(h) false)
2. SUPPORTS (S1)        -> requires PV >= 0.25 and CI lower > 0.10; not met
3. FALSIFIES (S0)       -> PV = 0.0435 <= 0.10
                           and clustered CI upper = 0.1163 < 0.25  => SELECTED
4. MIXED                -> not reached
```

## 6. Interpretation (bounded to this substrate and window)

`FALSIFIES` here means: on this credential-free action-gating substrate (frozen 57-endpoint pool, one credential-free stdlib-HTTP client, one time window), value-level predictability beyond a last-value memory baseline is rare (4.3%); the clustered upper bound (11.6%) is far below the 25% H1 threshold. Consistent with the preregistered negative consequence, this favours the **persist-procedures-and-paths, re-observe-values-fresh** side of the architecture decision over value-level memoization/replay for this class.

Per `spec.json.decision_rule.claim_ceiling`, this `FALSIFIES` outcome is bounded to the frozen credential-free action-gating substrate and window. It does **not** close `C-WEB-DYNAMICS` or the Physics domain, and it authorizes no Product promotion. `C-MEAS-VALID` and `C-CROSSSITE` receive no event from this packet.

## 7. Validity threats and representation loss

1. **Live-null construction correction (V1).** The first analysis bound each httpbin uuid to itself as a same-session cookie, making `R_SESSION_BIND` fire vacuously on 8/8 live-null fields. Rule predicates and all thresholds were unchanged; only the control's cookie-map construction was corrected to the faithful empty map (httpbin sets no cookies). The pre-correction artifact is preserved at `derived/controls_initial_live_null_selfbind_bug.json`.
2. **Author-authored positive control (V4).** Certifies the code path, not the real-Web construct boundary; mitigated by the out-of-author live null and the fresh real-Web collection.
3. **Pool/window (V5).** Not a probability sample of the Web.
4. **Representation loss (V6).** No JS/DOM/SPA/authenticated/edge/mobile/GraphQL token is observable; bodies archived only as sha256; the NONCE stratum has a single field.
5. **Rule multiplicity and attribution (V7).** 11 rules; class attribution can mislabel but does not affect the pooled indicator.
6. **Blocking/rate limits (V8).** Several endpoints returned 403/429; three census-admitted endpoints were unavailable this window. Admission still far exceeds the frozen minima.
7. **Client-side wall-clock (V3)** is the epoch source for wall-clock rules (+/-1 h tolerance).
8. **DESIGN/EXECUTE null-fire difference (V2)** bounds `R_WALLCLOCK_B64`'s FP rate only jointly with the DESIGN literal.

## 8. Artifacts and provenance

Raw evidence: `raw/collection.jsonl` (456 session records / 1368 observations, includes per-field raw values, status, session/request index, wall-clock epoch, body_sha256 and same-session cookie pairs). Derived measurements: `derived/fields.json`, `derived/field_cluster_map.json`, `derived/controls.json`, `derived/metrics.json`. Exact hashes are in `result.json.artifacts` and `provenance.json.code`.

## 9. Unresolved

- `U1_GENERALIZATION`: Do the two counted predictable classes persist across collection windows?
- `U2_CONSTRUCT_BOUNDARY`: What is the real-Web predictability prevalence on JS-rendered / authenticated / SPA substrates this instrument cannot observe?
- `U3_NULL_RULE_SENSITIVITY`: Why did R_WALLCLOCK_B64 fire once in the DESIGN literal null and zero times in the EXECUTE re-run with the same nominal seeds?
- `U4_REDDIT_MECHANISM`: What produces the constant 32-hex-character prefix of reddit.com jsc_token, and does it predict the suffix?
- `U5_VALUE_VS_PROCEDURE`: Does the bounded negative decide the product-level persist-values vs persist-procedures trade-off?

_Report generated by research/physics/exp_37973239386_finalize.py from the frozen packet and the EXECUTE raw/derived artifacts. It must not exceed the frozen claim or silently contradict result.json._
