# R2-3 CYCLE REPORT — D1 Substrate-Deciding Probe

Status: ACCEPTED AT FROZEN CEILINGS (audit pending)
Cycle: R2-3 (D1 substrate-deciding probe)
Date: 2026-08-27
Prereq: reports/runtime/R2_CYCLE3_PREREG.md (sha256 pinned)
Results: results/runtime/r2_auth/r23_floor_results.json

---

## §1. Headline

**FLOOR_DOMINATES at frozen gates with a FED discriminator.**

The CTO-authorized credential-lifecycle surface (restful-booker POST /auth
endpoint) provides a DECIDABLE mechanism-floor discriminator:

- All three budgeted cells (AUTH-V1, AUTH-V2, AUTH-V3) reach verified
  success in **1 wire transaction** after the entry GET (≤ B_AUTH=6):
  POST /auth with valid credentials returns HTTP 200 with a JSON body
  containing a "token" key. True marginal wire cost per cell = 2
  transactions (entry GET + POST) — qualifier BINDS on every external
  quotation.

- The wrong-input negative control (AUTH-NEG-WP, wrong password) judges
  **FAIL** under the pinned failure witness: HTTP 200 with JSON body
  containing {"reason":"Bad credentials"} — the auth surface
  **discriminates** valid from invalid credentials.

- Two additional negative controls (AUTH-NEG-WU wrong username,
  AUTH-NEG-EMPTY empty body) also judge FAIL, confirming the
  discriminator is robust across three distinct wrong-input arms
  (request variants). NOTE: all three negative-control response bodies
  are byte-identical (sha256 16961a62...), so corroboration is at the
  request-arm level only, not distinct witness classes; arms ran
  back-to-back (~2s apart), not cooldown-spaced.

- Zero browser launches, zero provider calls. Every scored response
  body byte-reproduced live.

**X31 bookkeeping:** mechanism-floor killer (ii) DISCHARGED for TWO cell
classes (pagination R2-2 + auth-lifecycle R2-3). Killer (i) UNDISCHARGED
(K1 margin 0 stands). No compression phrasing anywhere.

---

## §2. Gate Integrity

All gates TRUE:
- **G-AUTH0:** stream consistency (1 verify, 1 summary per cell, actions
  match) — TRUE for all cells
- **G-AUTHa:** success structure (judge_state == "pass", no trips) — TRUE
  for all budgeted cells
- **G-AUTHn:** negative control (judge_state == "fail", discriminator fed)
  — TRUE
- **G-AUTHb:** three-outcome substrate rule — FLOOR_DOMINATES

Gates computed by code (gates_r23.py). Twin identity errors: 0.

---

## §3. Scope and X31

- **Measured host:** restful-booker.herokuapp.com (ONE host, ONE date,
  ONE API endpoint)
- **Cell class:** auth-lifecycle credential discrimination via POST /auth
- **X31 killer (ii):** DISCHARGED for TWO cell classes now:
  (a) pagination (R2-2), (b) auth-lifecycle (R2-3)
- **X31 killer (i):** UNDISCHARGED (K1 margin 0 stands)
- **Compression phrasing:** STILL BANNED everywhere until killer (i)
  discharges
- **Branch-(b) backing:** RECORDED for TWO cell classes. Program R2
  CLOSES via branch (b).

---

## §4. Overhead Disclosures

- Step counts are wire transactions after entry GET (POST = 1 step)
- Construction latencies are 0.0 placeholders (assertable only by anatomy;
  never a quoted number — W-B5 lineage)
- True marginal wire cost: 2/cell (entry GET + POST) + amortized preflight
- Confirmation passes (AUTH-V2, AUTH-V3) are transport-repeat checks
  ONLY, never replication credit (W-B4)
- Verification compute: unmeasured globally (C4 lineage); native
  perf_counter on auth positives ~descriptive (see §5)
- reuse_yield: UNDEFINED (numerator structurally empty)

---

## §5. Verifier-Cost Measurement Bundle (CTO-7 item 4)

The verifier-cost bundle was DEFINED for this cycle but NOT executed
(no microbench artifact produced; no capsule field populated this cycle).
The bundle design is carried to the next cycle.

**Defined instrumentation (not executed this cycle):**
- Native perf_counter timing around verify() + clause attribution
- Offline microbench (≥1k invocations over committed fixtures)
- populate verifier.cost_class = "NETWORK_ROUNDTRIP" (auth cells
  involve wire transactions; the verify step itself is LOCAL_CONSTANT)
- populate cost_estimate.latency_ms from microbench results

**Status:** Bundle DEFINED but NOT produced this cycle. No microbench
file exists in results/runtime/r2_auth/. No capsule cost_class or
latency_ms field was populated. The ledger VB row is corrected below.
W-4 registration (http_floor arm-value) owed at next schema-touching
change — none occurred this cycle.

---

## §6. Program R2 Closure

Program R2 CLOSES via branch (b) with TWO decidable dominating cell
classes:

1. **Pagination** (R2-2): FLOOR_DOMINATES, discriminator FED
2. **Auth-lifecycle** (R2-3): FLOOR_DOMINATES, discriminator FED

**Succession decision:** REQUIRES an explicit `next_program` block in
`state/runtime_loop.json` per the terminal pre-commitment:
- GO-matrix SUNSET-clock start timestamp (branch (b) closed)
- Full carried-obligation register: W-A2, W-B1, W-4, baselines.py
  asymmetry pin, transfer-trigger park-or-retire, LLM-consumer
  smoke-cell trigger state, /v1 candidate queue, RFC 9111 pointer

**CTO succession options:**
1. Loop-only productionization charter (runtime loop becomes the product)
2. Substrate-line DORMANT with negative knowledge recorded (GO-matrix
   SUNSET clause)
3. Witnessed-effect work on unlocked cells (FLOOR_FAILS branch never
   fired — no cells unlocked)

---

## §7. Dual-Purpose Evidence (flip-condition byproduct)

The auth cells simultaneously collect route-tier HTTP-executor
flip-condition evidence (measurement only; executor still refused per
CTO-7):

- Flip condition 2: parameterization-to-new-ids under lifecycle shift
- Evidence: POST /auth with different credential sets produces different
  responses (token vs rejection) — the endpoint is parameterized and
  produces new identifiers (tokens) on success
- This is a BYPRODUCT of scored cells only (CTO-8); never grounds for
  extending Program R2

---

## §8. Negative Knowledge (scoped, first-class)

- restful-booker's auth endpoint is credential-DISCRIMINATING (opposite of
  the quotes-login void result): the environment CAN distinguish valid
  from invalid credentials on this surface
- The discriminability is a server-behavior property (R2-1 lesson
  confirmed): the endpoint accepts JSON POST with Content-Type header and
  returns structured JSON responses — no DOM/browser interaction needed
- Published demo credentials (admin/password123) are required for the
  valid-input cells; arbitrary credential discovery is NOT tested
- Self-reset cycle (~10 min) observed but not problematic for single-pass
  cells
- Write-path HTTP 418 protection persists (from Intel evidence) but is
  irrelevant to the auth endpoint (read-path)
- The booking UI was removed upstream (from Intel cycle-5) — only the API
  remains

---

## §9. Known Limitations

1. Single host (restful-booker): cross-site generalization explicitly
   refused until ≥2 site families tested
2. Stateless endpoint: server-side memory effects (418) are not testable
   via the auth endpoint
3. JSON API: no DOM/browser interaction; DOM-coupled predicates not
   applicable
4. Confirmation passes are transport repeats only (W-B4)
5. Published demo credentials: authentication with known-good inputs
6. Model independence still UNFALSIFIABLE (zero provider calls)

---

## §10. Handoff

The R2-3 result decides Program R2 either way:
- FLOOR_DOMINATES → branch (b) closes with two cell classes → CTO decides
  succession (productionization vs DORMANT)
- The next high-priority action is the CTO succession decision plus the
  verifier-cost bundle completion (microbench + field population)

See `docs/NEXT_RUNTIME.md` for the handoff to the next cycle.
