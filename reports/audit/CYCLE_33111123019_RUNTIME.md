# RUNTIME INDEPENDENT AUDIT — R2-3 (Runtime cycle 12) repair round 1

Auditor: RUNTIME INDEPENDENT AUDITOR (adversarial, read-only on team mount)
Assigned audit run id: 33111123019
Team run id under audit (per artifact): 33109369710
Repair round: 1
Mount: /tmp/spider_runtime_team  (tip 3506103 = "Runtime cycle 12 repair 1 attempt 1: team output")
Accepted base: current checkout `runtime-audit-base` (= origin/lab/runtime lineage; R2-2 accepted at 548709d)
Cycle scope: D1 substrate-deciding probe — does restful-booker POST /auth provide a decidable mechanism-floor discriminator outside the voided canon login?

GATE: **PASS** (safe_to_integrate: true, wording exactly as frozen ceilings). See `results/audit/CYCLE_33111123019_RUNTIME_GATE.json`.

---

## 0. What was audited (and what was NOT)

R2-3 is a **mechanism-floor / substrate-decidability** probe, NOT a work-compression or
capsule-production cycle. Its single verdict is `FLOOR_DOMINATES` (with a `FED` discriminator)
or one of its alternatives (`FLOOR_FAILS`, `FLOOR_VOID`, `CYCLE_INCONCLUSIVE`, `INVALID_ARM`).
The team explicitly does **not** claim work compression: `reuse_yield` is `UNDEFINED`
(numerator structurally empty) and X31 killer (i) is `UNDISCHARGED` (K1 margin 0 vs the
strongest scripted comparator). The audit therefore attacks the work-compression *frame* the
Runtime role requires, even though the team makes no positive compression claim, and verifies
the floor claim is not smuggled into one.

Recomputed / re-derived artifacts:
- `results/runtime/r2_auth/cost_events.jsonl` (25 rows)
- `results/runtime/r2_auth/r23_floor_results.json`
- `reports/runtime/R2_CYCLE3_PREREG.md` (sha256 pinned)
- `runtime/gates_r23.py`, `runtime/floor_auth.py`, `runtime/r2_cycle3.py`

NOT executed (to avoid mutating the team mount): `pytest` suite. Test file
`tests/runtime/test_floor_auth.py` was inspected for substance (tri-value, well-formed,
transport→unknown, success-mirror→VOID, budget anatomy, host allowlist, witness keys) and is
non-vacuous; the team's reported 264/264 is taken as reported, not independently rerun.

---

## 1. Recomputed headline

Independent recomputation of `gate_auth_cycle` over the committed `cost_events.jsonl`
(read-only import of team modules, output written only to `results/audit`):

```
OUTCOME               = FLOOR_DOMINATES
max_steps_observed    = 1
G_AUTH0_p5_all        = True
G_AUTHa_success_structure = True
G_AUTHn_negative_control_ok = True
derivation_errors     = []
twin_identity_errors  = []
cells: AUTH-V1 pass(1)  AUTH-V2 pass(1)  AUTH-V3 pass(1)
neg (AUTH-NEG-WP)     = fail  -> discriminator fed
extra neg AUTH-NEG-WU = fail  (request-arm corroboration)
extra neg AUTH-NEG-EMPTY = fail (request-arm corroboration)
```

This deep-matches the committed `r23_floor_results.json` analysis block (0 mismatches).
Prereg sha256 pin recomputed: `64e705a4…` == recorded. Failure-body sha256
`16961a6296…` == `printf '{"reason":"Bad credentials"}'` (28 bytes) == all three negative-control
bodies. So the headline `FLOOR_DOMINATES` is faithful to the evidence and the freeze was honored.

---

## 2. Work-compression recomputation (the role's core demand)

There is **no positive work-compression claim to recompute down**, but the frame was checked:

- `repeat_cost_ratio` vs the strongest scripted baseline (K1, from R1-1 quotes.toscrape.com,
  `runtime/r1_strong.py`): margin = 0 (SPIDER 4 actions == strong 4 actions on all four
  counterbalanced passes). So the mechanism floor does **not** beat the strongest comparator;
  `repeat_cost_ratio ≈ 1.0`. No compression survives.
- `reuse_yield` = `baseline_work_avoided / (retrieval + verification + maintenance)` is
  `UNDEFINED` (numerator structurally empty) — honestly stated, not a hidden zero.
- No capsule is produced this cycle (measurement arm only, by charter). Therefore no external
  agent can yet *consume* inherited work from R2-3; the "verified inherited work" product object
  is absent. This is by design (substrate probe; CTO succession decides productionization vs
  DORMANT) but it means the cycle demonstrates **mechanism reachability/decidability**, not
  cumulative work compression.

Conclusion: `FLOOR_DOMINATES` is a substrate/decidability verdict; it must never be quoted as a
speedup, margin, or work-compression result. The report and prereg ban compression phrasing and
the audit confirms no leakage of such language into claim, ledger, or state.

---

## 3. Attack catalogue (per RUNTIME_AUDITOR role)

### 3.1 Stale reuse / stale hits — NONE found
- The voided canon-login capsule (`runtime/quotes-login-route@v1`, FLOOR_VOID in R1) is
  explicitly avoided: D1 is "outside the voided canon login".
- Negative knowledge (report §8) correctly records that the restful-booker **booking UI was
  removed upstream** while the **auth API survived** — i.e. prior site knowledge was scoped and
  not blindly reused. No stale-hit dependence in the scored stream.

### 3.2 Context mismatch — NONE found
- The endpoint is a stateless JSON API; the success witness is a generic `token` key, not a
  fragile DOM/context predicate. No context-mismatch failure mode in the judge path.

### 3.3 Hidden answer leakage / internal-ID dependence — limitation, not a defect
- The success witness checks the literal `token` key (generic). The returned token is the
  *intended effect* (an auth token), not a SPIDER-internal store id; it is not leakage of the
  audit target.
- Flip-condition evidence (route-tier HTTP-executor condition 2: parameterization-to-new-ids)
  collects freshly minted tokens, but is explicitly **byproduct-only, refused for extending R2**
  (CTO-8). Not smuggled into the verdict.
- **Limitation (W-AUD-4):** the verified substrate evidence is NOT delivered as a
  model-agnostic, intent-addressable Capability Capsule. An external agent cannot currently
  consume it without knowing the endpoint/structure/run_id. The "external agent must not need
  internal IDs" guarantee holds at the probe level only; the resolver-facing contract is not
  produced this cycle.

### 3.4 Missing fallback — NONE (correct conservative fallbacks)
- Arm `_judge` order: transport error → `unknown`; success witness → pass; failure witness →
  fail; otherwise → `unknown`. On a negative control, a success-mirror → `FLOOR_VOID`
  (double-VOID precommitment). Gate `G-AUTHb` honors VOID-first precedence, then
  `CYCLE_INCONCLUSIVE`, then `FLOOR_DOMINATES`/`INVALID_ARM`/`FLOOR_FAILS`.
- **Robustness caveat (W-AUD-7):** if the API response *shape* drifts (e.g. a different error
  format with no `reason`/`token` key), the cell becomes `CYCLE_INCONCLUSIVE` rather than fail —
  correct conservative behavior, but it means the floor verdict can silently degrade to
  inconclusive on site drift. No freshness/TTL/invalidation signal is measured.

### 3.5 Expensive verification — gap disclosed (W-AUD-3)
- The verify step itself is a local JSON-key check (cheap). But the *full* verification path
  includes an entry GET wire transaction (overhead) and the global **verification compute is
  unmeasured** (C4 lineage). The verifier-cost measurement bundle was **DEFINED but NOT
  executed** this cycle (RF2 / ledger VB row): no microbench artifact, no `cost_class`, no
  `latency_ms` field populated. Because no compression claim is made, this does not defeat the
  floor claim, but it must be closed before any capsule is trusted for reuse economics.

### 3.6 Omitted maintenance overhead — disclosed (W-AUD-7)
- Live external API; no maintenance/re-verification cadence, TTL, or invalidation signal
  measured. Report §9 lists single-host, stateless, JSON, confirmation-pass, published-demo-
  credential, and model-independence-unfalsifiable limitations. All honestly disclosed.

### 3.7 Metric double counting — one quotient risk (W-AUD-5)
- The data separates `loads=1` (entry GET) from `steps=1` (POST), so no double count *inside*
  the result. But the headline "**1 wire transaction after the entry GET**" must always carry
  the true-marginal qualifier "= 2 transactions incl. entry". The report binds this (§1, §4) and
  the ledger repeats it. Bare quotation of "1 wire transaction" would undercount by the entry
  GET. Max-defensible wording keeps the qualifier.
- The three positive cells are the **same valid-input request repeated** (AUTH-V2/V3 =
  confirmation/transport-repeat passes, W-B4). "Three cells pass" must not be read as three
  independent positives. Max-defensible: one distinct valid-input case (admin/password123)
  replicated across 3 transport-repeat passes.

### 3.8 Evidence-tier inflation — NONE
- Observation tier correctly "ONE host, ONE date, ONE API endpoint". killer (ii) discharged for
  TWO cell classes but explicitly **not** compression. No site/class/agent/Web generalization.
- **Negative-control redundancy (W-AUD-2):** all three wrong-input arms return the *identical*
  28-byte body `{"reason":"Bad credentials"}` (sha256 `16961a62…`). They are therefore ONE
  distinct failure-witness class (binary invalid→Bad-credentials); the "discriminator robust
  across three distinct wrong-input arms" is true only at the request-arm level. RF3 already
  corrected the wording to "request-arm level only, not distinct witness classes"; this is
  confirmed and must not be elevated.

### 3.9 Run-id provenance mismatch (W-AUD-1)
- Audit assignment referenced run **33111123019**; the audited artifact records run
  **33109369710** (in `r23_floor_results.json` `run_note` and `state/runtime_loop.json`
  `github_run_id_audited`). RF1 already reconciled to 33109369710. 33111123019 is most plausibly
  the audit-harness run id. Provenance is internally consistent at 33109369710; both ids are
  recorded here so integration does not mislabel. Not a gate-blocker.

---

## 4. Required fixes (repair round 1 disposition)

RF1 (run-id reconciliation), RF2 (verifier-cost bundle reword — defined but not executed),
RF3 (failure-witness class wording corrected to request-arm level) are **all present and correct**
in the team snapshot's report/ledger/state. No new concrete required_fix blocks integration.
`required_fixes: []`.

---

## 5. Maximum defensible wording

On ONE host (restful-booker.herokuapp.com), ONE date (2026-08-27), ONE API endpoint
(POST /auth), bare HTTP reached verified success for the valid-input case (admin/password123) in
**1 wire transaction after the entry GET** (true marginal **2 transactions incl. entry GET**;
qualifier BINDS on every external quotation), replicated across 3 transport-repeat passes
(AUTH-V1/V2/V3 — confirmation passes, NOT replication credit), AND the wrong-input control
(AUTH-NEG-WP, wrong password) judged fail under the pinned failure witness (HTTP 200 JSON body
`{"reason":"Bad credentials"}`, well-formed-fail true); two additional wrong-input arms
(wrong username, empty body) also judged fail but all three negative-control bodies are
byte-identical (sha256 `16961a62…`), so corroboration is at the request-arm level only and does
NOT constitute three distinct failure-witness classes. Gate `FLOOR_DOMINATES` (discriminator
`FED` not voided) independently recomputed deep-equal from the committed event stream with twin
identity clean. Observation tier: ONE host, ONE date, ONE API endpoint. Mechanism-floor killer
(ii) DISCHARGED for TWO cell classes now (pagination R2-2 + auth-lifecycle R2-3); killer (i)
UNDISCHARGED (K1 margin 0 vs strongest comparator stands). NO compression / speedup /
work-compression / margin / novelty / reuse_yield claim is licensed by this cycle. The
verifier-cost measurement bundle was DEFINED but NOT executed (verification compute unmeasured).
No intent-addressable Capability Capsule or resolver contract was produced this cycle; the result
is substrate evidence only and must not be quoted as a delivered runtime capability, cross-site,
cross-model, or as cumulative work compression.

---

## 6. Handoff to Director / next agent

- Integrate at frozen ceilings; do not let any downstream text upgrade `FLOOR_DOMINATES` into a
  speedup or a capability.
- Carry W-AUD-1..W-AUD-7 plus the standing obligations (W-A2, W-B1, W-4, baselines.py pin,
  transfer-trigger park-or-retire, LLM-consumer smoke-cell, /v1 queue, RFC 9111 pointer).
- The CTO succession decision (loop-only productionization vs substrate-line DORMANT) remains
  open; if productionization is chosen, the auth floor must first become an intent-addressable
  capsule with measured verifier cost and a freshness/invalidation signal before it counts as
  verified inherited work an external agent can consume.
