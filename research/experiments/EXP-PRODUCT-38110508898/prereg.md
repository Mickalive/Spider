# EXP-PRODUCT-38110508898 preregistration

STATUS: DESIGN COMPLETE - awaiting independent design review and freeze (design_contract_version 2).

## 1. Purpose and mandate

This experiment discharges blocker B1 per the binding Global Director mandate (`request.json.director_mandate`): install the already-audited parameterized mechanism carrier **byte-identically** at the shipping kernel path `src/spider/kernel.py` and demonstrate, with a binding pre-freeze positive/negative certificate, that the installed shipping package:
(a) executes one known-positive inherited parameterized binding on an **UNSEEN held-out identifier** (`distill_parameterized` of three+ induction observations -> resolve EXECUTABLE with a correctly bound non-null action at confidence 0.9 -> deterministic fixture execute status 200 -> verify true);
(b) refuses one known-negative family of unsafe bindings (out-of-support / missing-parameter / wrong-intent) with a recorded reason and null bound action, returning **exactly `ResolutionStatus.UNKNOWN`** for the no-applicable-mechanism (wrong-intent) case;
(c) keeps the inherited-path counters honest; and
(d) keeps the installed identity equal to the frozen carrier git blob/sha256.

Promotion to Product Core is enabled **ONLY** on independent audit PASS. This experiment alone advances no claim status; its verdict is a blocker-discharge certificate feeding `C-PARAM-INHERIT`.

Parent handoff (EXP-PRODUCT-37989728440) is continuity evidence only; the Director mandate SUPERSEDES its four-arm next question. The prior task-bank certificate was unsatisfiable (B2 territory); this experiment is the orthogonal kernel-side install certificate.

## 2. Frozen identities (verified pre-freeze, 2026-10-11)

| Object | git blob | sha256 |
|---|---|---|
| Audited carrier kernel (reference) | `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796` | `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72` |
| Pre-install shipping kernel (`src/spider/kernel.py`) | `cfec98660b0277ccbf295e8a4119e8d81ddccf50` | `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61` |
| Audited models (`models.py`) | `f08608c36b1c7b536d553b690acd91cd63f590f7` | (record at EXECUTE; `src/spider/models.py` already equals it) |
| Audited registry (`registry.py`) | `986317f71c4a7d5506e3295991bc7217e2a8d2da` | (record at EXECUTE; `src/spider/registry.py` already equals it) |

Reference carrier path: `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py` (bound freeze artifact). The same directory's `models.py` and `registry.py` are also bound freeze artifacts. `tests/test_kernel.py` is bound (PC-EXACT-REPLAY regression identity).

Kernel semantics that the certificate relies on (all present in the audited carrier and probed pre-freeze):
- default `resolve()` execution threshold `min_confidence = 0.8`;
- literal `distill()` candidate confidence `0.5`;
- `distill_parameterized` of >= 2 (we use exactly 3) observations with at least one varying action field, inferring support by common-prefix narrowing to a char-class/length regex and the URL static-prefix + slot template;
- resolve loop: intents matching no registered mechanism return `ResolutionStatus.UNKNOWN` ("no applicable validated mechanism") before any refusal generation;
- counters: `retrieval_calls` incremented per resolve; `verification_calls` per verify; `repair_attempts` per rebind (rebind also performs a resolve, hence +1 retrieval); `model_calls = 0`, `model_tokens = 0`, `browser_actions = 0`, `latency_ms = 0.0` (kernel emits none of these).

## 3. Deterministic fixture (frozen recipe)

Stdlib-only local HTTP fixture, created by the EXECUTE harness inside the experiment directory:
- `http.server.ThreadingHTTPServer` bound to `127.0.0.1`, port `0` (ephemeral; the actual port is **recorded**, not part of the scientific identity).
- Handler: `GET /items/<3-digit-id>` -> `200` with JSON body `{"status":200,"item_id":"<id>","ok":true}`; any other path -> `404`.
- State is a pure function of the request path. No randomness, no session, no writes.

## 4. Certificate sequence (frozen; 8 steps, one kernel instance, one fresh trajectory)

Induction observations (available to `distill_parameterized`):
- `{"intent":"fetch-item","params":{"item":"142"},"action":{"method":"GET","url":"<fixture_base>/items/142"}}`
- `{"intent":"fetch-item","params":{"item":"937"},"action":{"method":"GET","url":"<fixture_base>/items/937"}}`
- `{"intent":"fetch-item","params":{"item":"508"},"action":{"method":"GET","url":"<fixture_base>/items/508"}}`

Certificate trace (statuses, reasons, confidence and counters are asserted EXACTLY as written):

| # | Call | Expected result | Counter effect |
|---|---|---|---|
| 1 | `distill_parameterized([obs142, obs937, obs508])` | mechanism M with `confidence == 0.9` (slot `item`, support `^[0-9]{3}$`, URL template `<fixture_base>/items/{item}`) | none |
| 2 | `resolve("fetch-item", ctx, {"item":"671"})` | `EXECUTABLE`, confidence `0.9`, `bound_action = {"method":"GET","url":"<fixture_base>/items/671","params":{"item":"671"}}` (671 is UNSEEN: not in {142,937,508}) | `retrieval_calls +1` |
| 3 | Execute bound_action with `http.client` against the fixture | `200`, body `{"status":200,"item_id":"671","ok":true}` | `http_requests +1` |
| 4 | `verify(M, {"status":200,"item_id":"671","ok":true}, {"item":"671"})` | `True` | `verification_calls +1` |
| 5 | `resolve("fetch-item", ctx, {"item":"12"})` | `EXPLORE`, `bound_action == None`, reason mentions the inferred support (out-of-support refusal) | `retrieval_calls +1` |
| 6 | `resolve("fetch-item", ctx, {})` | `EXPLORE`, `bound_action == None`, reason mentions missing required parameter | `retrieval_calls +1` |
| 7 | `resolve("no-such-intent", ctx, {})` | **exactly** `ResolutionStatus.UNKNOWN`, `mechanism_id == None`, `bound_action == None`, reason "no applicable validated mechanism" | `retrieval_calls +1` |
| 8 | `rebind("no-such-intent", ctx, {})` | `UNKNOWN` | `repair_attempts +1`, `retrieval_calls +1` |

Expected exact counter vector: `retrieval_calls=5, verification_calls=1, repair_attempts=1, http_requests=1, model_calls=0, model_tokens=0, browser_actions=0, latency_ms=0.0`.

Literal-null control (performed against the same installed kernel on a **separate** fresh trajectory): `distill([obs142])` -> candidate at confidence `0.5`; `resolve("fetch-item", ctx, {"item":"671"})` -> **EXPLORE**, `bound_action == None`, reason "candidate exists but confidence is below execution threshold". This is the B4 confidence-flow check: `0.5 < 0.8 <= 0.9`.

Pre-repair baseline (against the preserved pre-install bytes, no execution needed): `hasattr(pre_install_kernel_module, "distill_parameterized") == False` is asserted structurally (B5). The positive path is unreachable on the pre-repair kernel by construction.

## 5. EXECUTE protocol (binding)

1. **Preserve the pre-install state**: copy `src/spider/kernel.py` to `raw_evidence/pre_install_kernel.py`; record `git hash-object` and `sha256sum`; both MUST equal the pre-install identities in section 2.
2. **Verify bound artifacts unchanged** (freeze.json artifact_hashes): the three reference carrier files and `tests/test_kernel.py`. Any mismatch = MEASUREMENT_INVALID (external mutation), stop.
3. **Install byte-identically**: copy `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py` -> `src/spider/kernel.py` (plain byte copy; no edits, no reformatting).
4. **Verify installed identity (B0)**: `git hash-object src/spider/kernel.py` == `b15ed848...` AND `sha256sum` == `718efa6a...`; confirm `src/spider/models.py` == `f08608c3...` and `src/spider/registry.py` == `986317f7...` (these must be UNTOUCHED by EXECUTE); confirm `hasattr(spider.kernel, "distill_parameterized")` is True.
5. **Regression (PC-EXACT-REPLAY / B5)**: run `PYTHONPATH=src python3 -m unittest discover -s tests -v`; expect 3/3 pass against the installed kernel.
6. **Certificate run (B1-B4, B3)**: implement the EXACT 8-step sequence and literal-null control from section 4 in `harness/certificate.py` (stdlib only), using a fresh kernel instance and fresh counters per trajectory. Record every step outcome, reason, confidence, bound_action, and the final counter vector verbatim in `raw_evidence/certificate_trace.json`. The fixture base URL is derived at runtime (ephemeral port) and recorded in the trace.
7. **Record harness identity**: sha256 of `harness/certificate.py` into `result.json` artifacts and `provenance.json` (freeze.json cannot hash EXECUTE-created code; the bound carrier artifacts + frozen sequence pin semantics).
8. **Produce the packet**: `result.json` (exact required top-level shape), `report.md`, `provenance.json` per `research/EXPERIMENT_PACKET.md`; classify per section 7.

## 6. Satisfiability evidence (pre-freeze, non-outcome-bearing)

The full certificate was probed during DESIGN (2026-10-11) with stdlib-only code against the audited carrier (induction ids 142/937/508, held-out 671, api.example.com stand-in for the fixture URL):
- support inferred `^[0-9]{3}$`; held-out 671 (unseen) -> `EXECUTABLE` at `0.9`, bound `{"method":"GET","url":".../items/671"}`; verify True;
- `{"item":"12"}` -> EXPLORE, bound None, "parameter 'item' outside inferred support"; `{}` -> EXPLORE, bound None, "missing required parameter 'item'"; `"no-such-intent"` -> exactly UNKNOWN, mechanism None, bound None;
- literal `distill` -> 0.5 -> EXPLORE "candidate exists but confidence is below execution threshold" (null discriminates);
- counters honest per step (resolve +1 retrieval; verify +1 verification; rebind +1 repair +1 retrieval);
- simulated install into a temp package (carrier kernel + existing models/registry/__init__) imports fine and passes 3/3 existing tests.
A fresh EXECUTE or AUDIT can re-run this probe from the section 4 recipe; it is deterministic and contains no confirmatory outcome data (the probe IS the certificate recipe).

## 7. Outcome classification (binding)

- **SUPPORTS**: B0, B1, B2, B4, B5 PASS and B3 exact-vector PASS -> certificate satisfied; `promotion_ready = true` ONLY pending independent audit PASS. (`status=COMPLETE`)
- **FALSIFIES**: any of B0/B1/B2/B4/B5 fails -> certificate NOT satisfied; record the exact failing check and raw evidence; no promotion. (`status=COMPLETE`, negative outcome - a valid scientific negative, not an infrastructure failure)
- **MEASUREMENT_INVALID**: B3 fails (counter instrumentation integrity), OR any bound artifact mutated after freeze (identity verification fails against freeze.json artifact_hashes), OR fixture infrastructure cannot start (server exception, python < 3.11). Not a negative result; record the exact failure and the smallest unblocking action. (`status=MEASUREMENT_INVALID`)

## 8. AUDIT recomputation instructions

Independent AUDIT must: (1) verify the frozen artifact hashes still match; (2) recompute the installed identity (blob + sha256) and the pre-install preservation; (3) re-run `harness/certificate.py` (or re-derive the section 4 sequence from the bound carrier bytes) and independently assert every expected status/reason/confidence/bound_action and the exact counter vector; (4) confirm `model_calls==0 && model_tokens==0`; (5) confirm the regression suite passes; (6) reject any claim that promotion occurred without audit PASS. B3 exact-vector equality is checked by recomputation, not by trusting the producer trace.

## 9. Governance

- Frozen `request.json`/`spec.json`/`prereg.md` and freeze artifacts are immutable for EXECUTE/AUDIT.
- No self-promotion: the verdict records the certificate result; claim-status updates and promotion are Director/registry/finalizer decisions only.
- Any failure must preserve RAW EVIDENCE (pre-install bytes, installed bytes, certificate trace) and distinguish measurement failure from negative result.