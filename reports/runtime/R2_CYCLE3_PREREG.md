# R2-3 PREREGISTRATION — D1 Substrate-Deciding Probe

Status: FROZEN (sha256 computed at commit time; pinned below)
Frozen: BEFORE any live HTTP request of this cycle
Author: Runtime Runner (cycle R2-3, GitHub run TBD)
Supersedes: R2-2 prereg (reports/runtime/R2_CYCLE2_PREREG.md) by reference
            for transport/transport-layer patterns only

---

## §0. Question and branch structure

**Primary question:** Does the CTO-authorized credential-lifecycle surface
(restful-booker POST /auth endpoint) provide a wrong-input failure witness
strong enough to make the mechanism-floor discriminator DECIDABLE outside
the voided canon login?

**Terminal verdict classes (mutually exclusive, exhaustive):**

| Verdict | Meaning |
|---------|---------|
| FLOOR_DOMINATES | All budgeted cells judge_success within budget AND wrong-input control fails under pinned witness (discriminator DECIDABLE) |
| FLOOR_FAILS | ≥1 well-formed cell judges FAIL with negative control fed (floor falsified on expanded substrate; witnessed-effect POC unlocks) |
| FLOOR_VOID | Wrong-input control passes success verification OR feasibility void fires (environment accepts any credentials; double-VOID ends Program R2) |
| CYCLE_INCONCLUSIVE | Transport errors, health trips, missing evidence, malformed responses (never headroom evidence in either direction) |
| INVALID_ARM | All cells success but step budget breached (measurement failure, never scored) |

**CTO-8 double-VOID precommitment:** If feasibility probes show wrong
input does NOT verifiably fail, the SECOND VOID fires immediately (no
scored cells spent); Program R2 mechanism work ends honestly.

---

## §0.1. Inputs (hash-pinned committed state)

| Input | Source | Hash |
|-------|--------|------|
| Accepted R2-2 lane state | lab/runtime at 548709d | git tree |
| CTO-8 handoff | /tmp/spider_cto/docs/CTO_TO_RUNTIME.md | committed |
| CTO-7 GO matrix | directives/RUNTIME.md §CTO-7 | accepted |
| Intel restful-booker environment facts | Intel cycle-5-8 reports | accepted AUDITED_DURABLE |

---

## §1. Director rulings applied

- **R2-3-A (new):** CTO-7 GO matrix adopted as substrate authority; Chief
  CTO sole expansion keyholder; Runtime authors frozen lists in this prereg.
- **R2-3-B (new):** Control-feasibility probes mandatory pre-freeze (extends
  X29): valid MUST pass, wrong MUST verifiably fail, live, stdlib-class,
  receipts persisted (W-B2). DESIGN-FEASIBILITY tier, NON-EVIDENCE for
  scored outcomes.
- **R2-3-C (new):** (i) flip-condition evidence is byproduct of SCORED cells
  only; (ii) verifier bundle offline microbench runs UNCONDITIONALLY; (iii)
  valid-side feasibility-failure semantics frozen pre-probe; (iv) frozen
  lists SHOULD span ≥2 Class B hosts — single-host rationale below; (v)
  wrong-input arms span distinct failure witnesses; (vi) terminal
  next_program block carries SUNSET-clock + obligation register.

**Single-host justification (R2-3-C(iv) exception):** restful-booker is the
CTO-named candidate host. Class B sites from the demand spec
(the-internet.herokuapp.com, saucedemo.com) are reachable but their auth
endpoints have not been verified for discriminator viability. The CTO-8
 VOID-tiering amendment (corroboration across ≥2 distinct failure-witness
classes plus cooldown-spaced confirmatory) is satisfied by three distinct
wrong-input arms (wrong-password, wrong-username, empty-body) on the same
stateless host. If this host VOIDs, the double-VOID fires and Program R2
ends; no further host probing is needed. If this host DOMINATES, the
result is scoped to this host and cross-site generalization is explicitly
refused.

---

## §2. Cells (frozen enumeration)

### §2.1. Budgeted cells (valid credentials)

| run_id | credentials | description |
|--------|-------------|-------------|
| AUTH-V1 | {"username":"admin","password":"password123"} | valid credential pass 1 |
| AUTH-V2 | {"username":"admin","password":"password123"} | valid confirmation pass 1 |
| AUTH-V3 | {"username":"admin","password":"password123"} | valid confirmation pass 2 |

All three cells reach POST /auth with valid credentials. The expected
outcome is a 200 response with a JSON body containing a "token" key.
Confirmation passes (AUTH-V2, AUTH-V3) are transport-repeat checks
ONLY and must NEVER be counted toward REPLICATION/GENERALIZATION tiers
(W-B4).

### §2.2. Negative controls (wrong credentials; excluded from budget quantifier)

| run_id | credentials | description | expected outcome |
|--------|-------------|-------------|-----------------|
| AUTH-NEG-WP | {"username":"admin","password":"wrongpassword999"} | wrong password | fail (discriminator fed) |
| AUTH-NEG-WU | {"username":"nonexistent_user_xyz","password":"password123"} | wrong username | fail (distinct witness) |
| AUTH-NEG-EMPTY | {} | empty body | fail (edge case) |

Three distinct wrong-input arms span distinct failure witnesses per
R2-3-C(v): wrong-password (valid username, invalid password), wrong-
username (invalid username, valid password), empty-body (no credentials
at all). This satisfies the CTO-8 VOID-tiering corroboration requirement
(≥2 distinct failure-witness classes).

---

## §3. Hard-pinned witnesses

### §3.1. Success witness

Derived from DOCUMENTED restful-booker API contract (CTO-8 witness-
fitting circularity ban: valid-side iteration permitted pre-freeze).

```json
{
  "kind": "rt.tasks:restful_auth_success@v0",
  "token_key": "token",
  "host_allowlist": ["restful-booker.herokuapp.com"]
}
```

Judge state "pass" := parsed JSON response body contains a "token" key
(string value). X33 tier: STATE_WITNESS (verifies the goal-state effect:
successful authentication producing a bearer token).

### §3.2. Failure witness

Derived from DOCUMENTED restful-booker API contract (CTO-8: NO live
iteration for wrong-input side; witness frozen before first request).

```json
{
  "kind": "rt.tasks:restful_auth_failure@v0",
  "reason_key": "reason",
  "reason_substring_ci": "Bad credentials",
  "host_allowlist": ["restful-booker.herokuapp.com"]
}
```

Judge state "fail" := parsed JSON response body contains a "reason" key
whose value (case-insensitive) contains "Bad credentials".
X33 tier: STATE_WITNESS (verifies the failure-state effect: credential
rejection with specific error signature).

**CTO-8 witness-fitting circularity ban:** The failure witness above is
derived from the DOCUMENTED API behavior (restful-booker public API docs
state that invalid credentials return {"reason":"Bad credentials"}).
No live iteration against candidate witnesses is performed for the
wrong-input side. The valid side is iterated pre-freeze per CTO-8 §0.1.

---

## §4. Procedure per cell

### §4.1. Budgeted cells (AUTH-V1, AUTH-V2, AUTH-V3)

1. T0: Entry GET https://restful-booker.herokuapp.com/ (LOAD analogue;
   not a step; health-floored: status 200 required)
2. T1: POST https://restful-booker.herokuapp.com/auth with JSON body
   {"username":"admin","password":"password123"}; Content-Type: application/
   json; 1 step
3. Manual redirect walk (each hop 1 step; expected: none)
4. Judge on FINAL response: parse JSON; check "token" key presence → pass

### §4.2. Negative controls (AUTH-NEG-WP, AUTH-NEG-WU, AUTH-NEG-EMPTY)

1. T0: Entry GET https://restful-booker.herokuapp.com/ (LOAD analogue)
2. T1: POST https://restful-booker.herokuapp.com/auth with JSON body
   per §2.2 credentials; 1 step
3. Manual redirect walk (expected: none)
4. Judge on FINAL response: CTO-8 frozen order:
   - Transport error → unknown (inconclusive)
   - Success witness ("token" key present) → pass → FLOOR_VOID
   - Failure witness ("reason" containing "Bad credentials") → fail
   - Otherwise → unknown (inconclusive)

---

## §4.3. Budget

B_AUTH = 1 + MAX_REDIRECT_HOPS = 1 + 5 = 6

Step unit = one outbound wire transaction after the entry GET.
Construction latency = 0.0 placeholder (assertable only by anatomy;
never a quoted number — W-B5 lineage).

True marginal wire cost per cell = 2 transactions (entry GET + POST)
+ amortized preflight. Qualifier BINDS on every external quotation.

---

## §5. Gates and decision rule

### G-AUTH0 — stream consistency per cell
Exactly one verify row (row_id == run_id), exactly one summary row,
summary cost.actions == wire-transaction steps (actN rows).

### G-AUTHa — success structure per budgeted cell
JUDGE_SUCCESS(c) := tri-value judge state == "pass" AND no recorded trip.

### G-AUTHn — wrong-input control tri-value
- judge "fail" → control OK (discriminator fed)
- judge "pass" → success mirror → FLOOR_VOID (second void candidate)
- judge "unknown" → transport/ambiguous → CYCLE_INCONCLUSIVE

VOID precedence is FIRST.

### G-AUTHb — three-outcome substrate rule
- FLOOR_DOMINATES iff all budgeted cells JUDGE_SUCCESS and max(steps) ≤ B_AUTH and negative control fails
- INVALID_ARM iff all cells success but max(steps) > B_AUTH
- FLOOR_FAILS iff ≥1 well-formed FAIL cell with no inconclusive cells
- CYCLE_INCONCLUSIVE otherwise

---

## §6. Preflight (pre-freeze, design-feasibility only)

### §6.1. Feasibility probes (CTO-8 mandatory, NON-EVIDENCE)

Cumulative live-request cap frozen at 6:
1. Host root GET (https://restful-booker.herokuapp.com/)
2. Valid-input POST (admin/password123) — valid side iteration OK
3. Wrong-password POST — from documented contract, no iteration
4. Wrong-username POST — from documented contract, no iteration
5. Empty-body POST — from documented contract, no iteration
6. Reserved

Receipts persisted at results/runtime/r2_auth/feasibility/
feasibility_receipts.json.

Feasibility verdict:
- valid passes AND wrong fails → proceed to scored cells
- wrong does NOT fail → DOUBLE-VOID fires; Program R2 ends; no scored cells

### §6.2. Blinding preflight
Channel-1 scan of floor_auth.py and gates_r23.py against frozen fixture.
These modules carry no predicate-ref strings by construction.

---

## §7. Pre-freeze observations (advisory, non-evidence)

From Intel cycle-5-8 accepted evidence:
- restful-booker's root page is a static welcome page (booking UI removed)
- API remains public: POST /auth, GET /booking, etc. work
- Published demo credentials: admin/password123
- Self-resets every ~10 minutes
- Write-path HTTP 418 protection observed under repeated scripted traffic
  (irrelevant to auth endpoint which is read-path)

Expected outcome: FLOOR_DOMINATES (auth endpoint discriminates by design;
the host contract explicitly returns different responses for valid vs
invalid credentials).

---

## §8. Analysis plan

1. Compute twin-identity errors on committed stream
2. Run gate_auth_cycle() on committed stream
3. Report outcome per §5
4. Record flip-condition evidence from scored cells (byproduct only; never
   grounds for extending R2 — CTO-8)
5. Persist MIXED aggregation row (single host this cycle; trivial)

---

## §9. Wording ceilings and refusals

- No compression phrasing anywhere (killer (i) undischarged — X31)
- "1 wire transaction" excludes entry GET (W-B5 lineage); true marginal
  wire cost = 2/cell + amortized preflight
- Confirmation passes are transport-repeat checks, never replication credit
  (W-B4)
- No floor figure quoted without steps-after-entry-GET qualifier (W-B5)
- Construction latency = 0.0 placeholder, never a quoted number
- Flip-condition evidence is a BYPRODUCT of SCORED cells only (CTO-8)
- Scope: ONE host, ONE date, ONE API endpoint; never "all auth endpoints",
  never "the Web"
- reuse_yield stays UNDEFINED (numerator structurally empty)
- model independence still UNFALSIFIABLE (zero provider calls)

---

## §10. Disclosed limitations

1. Single host (restful-booker): cross-site generalization explicitly
   refused until ≥2 site families tested
2. Stateless endpoint: server-side memory effects (observed on write-path)
   are not testable via auth endpoint
3. JSON API: no DOM/browser interaction; DOM-coupled predicates not applicable
4. Confirmation passes (AUTH-V2, AUTH-V3) are transport repeats only
5. Published demo credentials: authentication is with known-good inputs,
   not arbitrary credential discovery
6. Self-reset cycle (~10 min): cells must complete within a single
   reset window for determinism

---

## §11. Verifier-cost measurement bundle (CTO-7 item 4, riding same harness)

This bundle is UNCONDITIONAL per R2-3-C(ii): the offline microbench half
executes even if feasibility VOIDs before any scored cell.

### §11.1. Native perf_counter timing
- verify() positive-case timing via perf_counter spans
- Clause attribution (which predicate clause dominates verify time)

### §11.2. Offline microbench
- ≥1,000 invocations over committed registry fixtures
- Report median, p95, share-of-e2e
- Populate verifier.cost_class and cost_estimate.latency_ms
  (existing nullable fields; instrument tier; W-4 registration at
  next schema touch)

### §11.3. cost_class enum
Per CTO-8: LOCAL_CONSTANT | NETWORK_ROUNDTRIP | BROWSER_ACTION |
PROVIDER_CALL. Auth cells are NETWORK_ROUNDTRIP.

---

## §12. Terminal pre-commitment (Program R2 ends after R2-3 either way)

Per directives/RUNTIME.md:

- **D1 FLOOR_DOMINATES:** R2 CLOSES branch (b) with two decidable
  dominating cell classes (pagination + D1). CTO decision: loop-only
  productionization charter vs substrate-line DORMANT (GO-matrix SUNSET).
  next_program block must carry SUNSET-clock start + full obligation
  register (W-A2, W-B1, W-4, baselines.py pin, transfer-trigger
  decision, LLM-consumer smoke-cell state, /v1 candidate queue, RFC 9111).

- **D1 FLOOR_FAILS:** Falsifies domination on expanded substrate;
  witnessed-effect POC unlocks on those cells; R2 continues.

- **D1 FLOOR_VOID (feasibility or scored):** double-VOID fires;
  mechanism work ends honestly; convert to escalation support +
  loop-only productionization question.

- **CYCLE_INCONCLUSIVE / INVALID_ARM:** repair-first (one repair round,
  then void-class consequences apply honestly).
