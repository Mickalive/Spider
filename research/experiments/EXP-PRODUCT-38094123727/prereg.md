# EXP-PRODUCT-38094123727 preregistration

Status: DESIGN COMPLETE, NOT YET FROZEN (this file is the DESIGN deliverable; the immutable `freeze.json` is written by `scripts/freeze_experiment.py` only after the design-review agents pass the six checks and `design_review.json` is written).

Lane: product · Claim: C-PARAM-INHERIT · Design contract version: 2 · Mode: DESIGN (no outcome-bearing measurement was executed; only satisfiability probes, section 8).

---

## 1. Mandate, inheritance and scope

- Immutable direction: `research/experiments/EXP-PRODUCT-38094123727/request.json` (`request_hash` a24f8766…), `director_mandate.allocation.action=CONTINUE`, target claim `C-PARAM-INHERIT`. The mandate's strategic question: land the audited parameterized inherited carrier into the shipped kernel **through the sanctioned promotion path** (blocker B1, `research/portfolio/PROGRAM_AUDIT_2026-10-10.md`) so that, after promotion, the shipped execution path contains a concrete parameterized mechanism that an inherited procedure visibly instantiates and executes, together with a companion known-negative refusal certificate.
- The mandate **explicitly does NOT fund** the four-arm COLD/INSTRUCTIONS/RETRIEVAL/SPIDER economics benchmark this cycle (`allocation.rationale`); readiness conditions (2)/(3) do not hold. This experiment therefore contains **no benchmark arms** (integrity check I-C9). It is not a re-run of any pre-2.0 economics certificate.
- Parent handoff (`research/experiments/EXP-PRODUCT-37989728440/handoff.json`) is dispositioned SUPERSEDE by the mandate. Its carry-forward that remains load-bearing here:
  - *established*: carrier identity (git blob `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796`, sha256 `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`); shipped `src/spider/kernel.py` = blob `cfec98660b0277ccbf295e8a4119e8d81ddccf50` (sha256 `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61`), literal-only, confidence 0.5 < 0.8 default threshold; B-LITERAL-KERNEL 0.0 vs PC-EXACT-REPLAY 20/20 on this carrier (instrument discrimination); the support-predicate workaround (held-out values kept inside the induced support grammar — the substrate was engineered for this, the kernel was not fixed).
  - *rejected / do_not_assume*: do not treat prior 1.0-ceiling cold/retrieval results as evidence against inheritance; do not re-run the mandatory-discovery deterministic REST certificate (three consecutive saturated runs); do not claim latency economics (deterministic counters only); do not promote prior packet code; do not generalize the support workaround into a support-generalization result.
- Inheritance from the failed B1 designs (EXP-PRODUCT-38085188374, EXP-PRODUCT-38078422511, EXP-PRODUCT-38074828779): all three failed at the design-review stage (model pool/provider), never froze, and produced no outcome evidence; their repeated DESIGN failure fingerprint is a control-plane issue, not a scientific outcome — but this design deliberately reduces reviewer load (single real tier, no synthetic F1–F6 tier, no over-wide decision table) so the design-review pool has a smaller, denser object to evaluate.

## 2. Claim, hypothesis, falsifier

- **Claim**: C-PARAM-INHERIT — the parameterized carrier mechanism is inheritable by a shipped executable path with a companion known-negative refusal path. (Effective status retained: EXPERIMENTAL, `codex/claim_state.json`; no advance without a verdict.)
- **Hypothesis (frozen)**: installing the audited carrier **byte-identically** into `src/spider/kernel.py`, with the shared modules `src/spider/models.py`, `src/spider/registry.py`, `src/spider/__init__.py` untouched and byte-identical to the audited copies, makes the shipped kernel (a) induce exactly 4 parameterized mechanisms (one per family×resource-type pair) at confidence 0.9 with support-constrained parameter slots from the frozen training observations, (b) resolve EXECUTABLE and complete **10/10 held-out novelty-0.0 update_resource tasks** with new identifiers on the frozen credential-free real-HTTP substrate with postconditions verified over the live socket and **zero fallback**, (c) refuse **30/30 known-negative probes** (out-of-support identifier / missing parameter / wrong intent) with `bound_action=null` and the correct status/reason category, while (d) the byte-delimited counterfactual holds: the pre-install kernel on sha256-identical shared modules is support-blind (over-accepts `doc-999` as EXECUTABLE), cannot induce the parameterized path (AttributeError), and emits only 0.5-confidence literals below the 0.8 threshold; and (e) the whole promotion delta (`src/spider/kernel.py` + one new regression test) passes compileall + the full unittest discovery suite + `validate_repo.py` within the Product lane's allowed code roots.
- **Falsifier (frozen)**: F1 — not 4/4 mechanisms induced from the frozen training observations, or any canonical mechanism serialization differs from the vendored-reference induction, or fewer than 10/10 held-out tasks EXECUTABLE-and-complete (or any fallback needed); F2 — refusal battery not 30/30 null-bound with expected category status/reason; F3 — pre-install kernel fails to over-accept (no discriminating pair) or the pre-install bytes already contain a refusal/parameterized path; F4 — promotion suite does not pass on the delta. Any F1–F4 with valid measurements ⇒ outcome=FALSIFIES, no promotion, claim retained EXPERIMENTAL. Identity/drift/infrastructure failures ⇒ status=MEASUREMENT_INVALID (this is a measurement failure, never a scientific negative).

## 3. Design

- **Treatment**: T-SPIDER-PARAM-SHIPPED — `src/spider/kernel.py` = carrier bytes (blob `b15ed848`, sha256 `718efa6a…`), i.e. `SpiderKernel.distill_parameterized()` + `resolve()` with support predicates + `TrajectoryCounters`.
- **Comparator (baseline)**: B-PREINSTALL — `src/spider/kernel.py` = shipped bytes at `request.base_sha` (blob `cfec9866`, sha256 `46929b3a…`) loaded in isolation (git bytes + unchanged `src/spider` models/registry/__init__), never written into the live package. Contrast: B-PREINSTALL-LITERAL (cannot induce; 0.5 literals) and B-PREINSTALL-OVERACCEPT (support-blind EXECUTABLE on `doc-999`).
- **Controls**: PC-PARAM-BINDING (positive: hand-authored mechanism in an emptied registry of the installed kernel must resolve EXECUTABLE with the correct bound action URL) and NC-EMPTY-REGISTRY (null: emptied registry on a positive-shaped task must resolve UNKNOWN, `bound_action=null`). NC-REFUSAL-NULL: all 30 battery trials must have `bound_action=null`. Inherited instrument anchor (not re-run): PC-EXACT-REPLAY 20/20 vs B-LITERAL-KERNEL 0.0 (EXP-PRODUCT-37989728440).
- **Contrast with pre-2.0 precedents**: P2-REPLAY-COST / P2-BLIND-COMPOSITION / P2-MIND2WEB are literal/scripted legacy results; this experiment ships a parameterized identifier-general mechanism through the production promotion path with a refusal certificate — a materially distinct extension (per `allocation.comparative_reasoning`), not a replay benchmark.
- **Contrast with the three prior B1 designs**: dropped the synthetic F1–F6 replication tier (out of scope for the mandate; the real tier carries the claim), kept one discriminating real tier, and made every gating core satisfiability-probed before freeze (section 8).

## 4. Frozen inputs and artifact binding (immutable interpretation dependencies)

All 9 freeze artifacts are `freeze.json.artifact_hashes`; EXECUTE must verify them before and after the run and must not modify them:

| Path (repo-relative) | sha256 (design-time, verified) |
|---|---|
| `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/kernel.py` | 718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72 |
| `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/models.py` | 338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78 |
| `research/experiments/EXP-PRODUCT-37989728440/harness/audited_spider/registry.py` | 51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c |
| `research/experiments/EXP-PRODUCT-37989728440/harness/substrate.py` | 0f9f9182cb90ac9e379000e4420a93ba2d2e6a167906c59bd9eac8a8392395af |
| `research/experiments/EXP-PRODUCT-37989728440/harness/run_experiment.py` | 4cb974e8ba7fd7dc15596be53b40256a658607a2a3a36ec735468fcb3132442b |
| `src/spider/models.py` | 338aaf4d7ba0e31f7a5fe8a47abdbb2ea52d9c1c4ef0ce014f2b809b9a2a9b78 |
| `src/spider/registry.py` | 51fb440d3827f21cccb5f77ad17dc0e76ccdbc2d52d7b05044cd821bb8a9322c |
| `src/spider/__init__.py` | 3d173722b38c5130a5145b1558412a399f851c8ed4fbf2ddfa4022e4cb2b5a77 |
| `tests/test_kernel.py` | ff9c1561c4169d306fba56d52442546a3bbfdab11d3ab56c51d7369309e9c0b6 |

Byte pins that bracket the mutable deliverable (NOT freeze artifacts, by design):
- pre-install shipped kernel: git blob `cfec98660b0277ccbf295e8a4119e8d81ddccf50`, content sha256 `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61`, reachable at `request.base_sha` = `6b4a1f7b18e84015e1765965081f2a8e97d3ba27`.
- post-install (mutable target `src/spider/kernel.py`): carrier git blob `b15ed8487e2d1326df4ca64fb4c7b6e5a0ebf796`, content sha256 `718efa6a167c2fdc483a8fbaaf1a05ce018dcb1c52808414b2a6a76d788bfb72`.

Because the freeze cannot hash the deliverable, the binding is explicit: EXECUTE records `pre_execute_sha` (via the workflow checkpoint) and must verify that `git diff request.base_sha..pre_execute_sha -- src tests sdk pyproject.toml` is **empty** (verified at design time: the allocation commit 0ddd9f6c touches only `research/`); any code-root drift between request time and EXECUTE start ⇒ MEASUREMENT_INVALID (G0).

## 5. Frozen substrate recipe (real tier, one certificate)

From `substrate.py` (frozen, sha256 0f9f9182…):
- Credential-free localhost stdlib-HTTP server; SEED=42; single-threaded client; transport 127.0.0.1 only. Server contract: `GET /api/session` (→ `{"session_token","expires"}`), `GET /api/resources`, `GET /api/schema/<type>`, `POST /api/<type>/<id>/update` (requires `X-Session-Token` header when the scenario enforces it; body `{"property":..., "value":...}` → `{"success":true,"type","id","property","value"}`).
- Families: F1 {documents→prefix `doc`, records→`rec`}, F2 {widgets→`wid`, gadgets→`gad`}. Task types per family cycle `properties`.
- Training capture (20 tasks): `build_train_tasks()` — novelty 0.0, ids `(i+1)*11` → 011/022/033/044/055 per type; token per task; property cycles the family's list; value `draft-{j}` j=0..4.
- Held-out positive set (10 tasks): `build_test_tasks()` filtered to `novelty_fraction==0.0` — ids `(i+1)*13` → 013/026/039/052/065 per type (all strictly inside the induced support), values `draft-5..draft-9`, properties from the family list.
- One single `SubstrateServer` instance for the **entire** certificate: mechanisms' action templates embed the live `base_url` (port), so induction and all executions must share one bound base_url.
- Support grammars the carrier induces on this substrate (probe-verified, section 8): `session_token → ^tok\-[a-z0-9]{16}$`, `property → ^[a-z]+$`, `value → ^draft\-[0-9]{1}$`, id slot → `^<prefix>\-0[0-9]{2}$` (`prefix` ∈ {doc, rec, wid, gad}). All held-out 0.0 values are inside these grammars by frozen construction.

## 6. Frozen procedures (EXECUTE recipe)

Order of operations (deterministic, single run):

1. **Preconditions (G0)**: verify 9/9 freeze artifact hashes; verify `git diff base_sha..HEAD` empty over allowed roots; record `pre_execute_sha`; snapshot pre-install kernel bytes/notes (expect blob cfec9866 / sha256 46929b3a) from `git show base_sha:src/spider/kernel.py`; record installed-kernel absent state.
2. **Install**: overwrite `src/spider/kernel.py` with the carrier bytes read from the frozen artifact (equivalently `git show b15ed848`); verify new sha256 == 718efa6a… and the resulting tree has `src/spider/models.py|registry.py|__init__.py` unchanged.
3. **Write regression test** `tests/test_ship_kernel.py`: (a) `SpiderKernel` exposes `distill_parameterized`; (b) a parameterized mechanism with support grammars refuses an out-of-support identifier (EXPLORE, `bound_action is None`) while accepting an in-support one (EXECUTABLE); (c) literal `distill()` output stays below the 0.8 threshold (EXPLORE). This test must pass both in-lane (post-install) and post-promotion on main.
4. **Train capture + induction**: start one server; iterate `build_train_tasks()`; per task do `GET /api/session` then the `POST /api/<type>/<id>/update` per task spec; record `Observation(intent="update_resource", state={family, resource_type, base_url}, action, next_state=response_body, success=True)`. Group by (family, resource_type) → 4 groups of 5 observations. Induce one mechanism per group with the vendored-reference kernel (loaded from the frozen artifact) and with the installed kernel (`import spider.kernel` after install); require 4/4 mechanisms, and require canonical `as_dict()` sha256 equality between the two inductions (fidelity).
5. **Positive execution (G1)**: for each of the 10 held-out novelty-0.0 tasks: `GET /api/session` (token), `resolve("update_resource", context={family, resource_type, base_url}, params={session_token, property, value, <id>})` → require EXECUTABLE with `mechanism_id` prefix `mech-` and confidence 0.9; execute the bound `POST` over the real socket; require HTTP 200 and `_matches(bound_postconditions, body)`. No discovery of id/endpoint, no repair, no cold fallback (any fallback disqualifies the task, M4).
6. **Refusal battery (G2)**, resolve-level only (no HTTP for refuse cases, M5): 30 trials over the 4 induced mechanisms — (A) 10 out-of-support identifier (e.g. `doc-999`, `rec-999`, `wid-999`, `gad-999` cycled) → expect EXPLORE, reason `parameter '<id>' outside inferred support`; (B) 10 missing required parameter (omit the id slot) → expect EXPLORE, reason `missing required parameter '<id>'`; (C) 10 wrong intent (`intent="get_session"` against update mechanisms) → expect UNKNOWN, reason `no applicable validated mechanism`. All 30 must have `bound_action=None`.
7. **Pre-install discrimination (G3)**: build an isolated temp package `{__init__.py, models.py, registry.py}` from `src/spider/` + `kernel.py` from `git show base_sha:src/spider/kernel.py`; upsert one induced mechanism into its registry; resolve `doc-999` → require EXECUTABLE (support-blind over-accept). The installed kernel on the same probe → require EXPLORE. Literal floor: run pre-install `distill()` over the 5 (F1, documents) training observations → require every literal at confidence 0.5 → resolve → EXPLORE (below 0.8).
8. **Controls**: PC-PARAM-BINDING (emptied registry + hand-authored mechanism, resolve `doc-026` → EXECUTABLE with correct bound URL — requires `GET /api/session` for the token param + a live `POST` confirm); NC-EMPTY-REGISTRY (emptied registry, positive-shaped params → UNKNOWN, null bound).
9. **Promotion suite (G4)**: `python -m compileall -q src scripts`; `PYTHONPATH=src python -m unittest discover -s tests -v` (3 inherited + new test); `python scripts/validate_repo.py`; `git diff --name-only base_sha..HEAD -- src tests sdk pyproject.toml` must equal exactly `src/spider/kernel.py`, `tests/test_ship_kernel.py`.
10. **Derived measurements + decision rule**, then `result.json` / `report.md` / `provenance.json` (RAW EVIDENCE → OBSERVATION → MEASUREMENT → INTERPRETATION kept distinct; raw task trajectories, counters, induced mechanisms, refusal records all persisted under `raw_evidence/`, hashes in provenance).

## 7. Metrics (derived, frozen names — EXECUTE must emit exactly these keys)

`m_install_identity` (sha256(src/spider/kernel.py)==718efa6a… AND git blob b15ed848), `m_induced_mechanisms` (==4), `m_mechanism_fidelity` (==4/4 canonical-as_dict sha256 matches vs vendored-reference induction), `m_heldout_executed` (==10/10, no fallback), `m_refusal_rate` (==30/30 with per-category counts), `m_preinstall_overaccept` (true: doc-999 EXECUTABLE pre-install), `m_installed_refuses_oos` (true: doc-999 EXPLORE installed), `m_literal_floor` (all literal confidences ==0.5), `m_promo_suite` ({compileall, unittest, validate_repo} all pass), `m_delta_scope_ok` (true), `m_model_calls` (==0), `m_model_tokens` (==0), `m_real_http_cycles` (exact count of socket request/response pairs, ~62), `m_retrieval_calls` (per-resolve instrumentation, not economics), `m_no_benchmark` (true). Controls emitted as `PC-PARAM-BINDING`, `NC-EMPTY-REGISTRY`, `NC-REFUSAL-NULL` with their statuses.

## 8. Pre-freeze satisfiability probes (non-outcome-bearing; run at DESIGN time in /tmp, results below)

These probes established *reachability* of every gating code path with non-confirmatory inputs (training identifiers and refusal-shape inputs); the confirmatory 10/10 held-out outcome and the 30/30 aggregate battery were NOT executed during DESIGN.

- Probe P1 (induction + liveness): `distill_parameterized` on the 20 real captured training observations induced exactly 4 mechanisms, all confidence 0.9, slots `[session_token, property, value, <id>]`, supports `^tok\-[a-z0-9]{16}$ / ^[a-z]+$ / ^draft\-[0-9]{1}$ / ^<prefix>\-0[0-9]{2}$`; resolve of in-support `doc-011` → `EXECUTABLE`, bound URL `http://127.0.0.1:<port>/api/documents/doc-011/update`.
- Probe P2 (refusal statuses): `doc-999` → EXPLORE `parameter 'document' outside inferred support`; missing id param → EXPLORE `missing required parameter 'document'`; wrong intent → UNKNOWN `no applicable validated mechanism`; out-of-support value `final-draft` → EXPLORE `outside inferred support`; all with `bound_action=None`.
- Probe P3 (pre-install counterfactual): bytes of `git show base_sha:src/spider/kernel.py` lack `distill_parameterized` (AttributeError on call); with the induced mechanism upserted, pre-install resolve of `doc-999` → **EXECUTABLE** (support-blind over-accept); pre-install `distill()` literals all confidence 0.5 (<0.8 → EXPLORE).
- Probe P4 (controls): PC-PARAM-BINDING → EXECUTABLE with correct bound URL; NC-EMPTY-REGISTRY → UNKNOWN, null bound.
- Probe P5 (suite reachability): `python -m compileall -q src scripts` OK; `PYTHONPATH=src python -m unittest discover -s tests -v` → 3/3 pass against BOTH shipped and carrier kernels; `python scripts/validate_repo.py` → `SPIDER_R2_VALIDATE_OK`; git blob/`base_sha` objects present; code-root diff base_sha→HEAD empty.
- Denominator arithmetic: held-out 0.0 ids (1-based ×13) are all inside `^<prefix>\-0[0-9]{2}$`; values `draft-5..9` inside `^draft\-[0-9]{1}$`; tokens inside `^tok\-[a-z0-9]{16}$` — 10/10 is arithmetically reachable, ceiling/floor are not touched (no arm at 1.0 on this certificate; the refusal floor 0/30 vs target 30/30 is discriminating).

## 9. Decision rule (frozen, mirrors spec.json.decision_rule)

Evaluate gates in order; record each gate's inputs and result raw:

- G0 INSTALL-IDENTITY — fail ⇒ status=MEASUREMENT_INVALID, outcome=INVALID (report exact blocker; no promotion).
- G1 REAL-POSITIVE → G2 REFUSAL-CERTIFICATE → G3 PREINSTALL-DISCRIMINATION → G4 PROMOTION-SUITE — any fail with valid measurements ⇒ status=COMPLETE, outcome=FALSIFIES (negative is first-class; no promotion; claim retained EXPERIMENTAL).
- All PASS ⇒ status=COMPLETE, outcome=POSITIVE; packet recommends audit PASS and `promote_to_product=true`; the sanctioned workflow (`product-promote.yml`) then promotes the delta `base_sha → verdict-commit` restricted to `src tests sdk pyproject.toml`, re-runs compileall + validate_repo + unittest on main, and ships.
- Integrity checks I-C5/I-C6/I-C7/I-C8/I-C9 are recorded but do not by themselves flip the outcome; a failed I-C7 (any model call) or I-C9 (benchmark arm ran) is a governance violation recorded as a blocking finding.

## 10. Measurement validity & honesty constraints

- Outcome-bearing evidence is real-HTTP-only (M1); deterministic single run, single server instance, `SEED=42` (M2); byte-level identity pins and 9/9 artifact hashes before+after (M3); no-fallback counting (M4); resolve-level refusals with null-bound verification (M5); zero model/browser/external-network by construction, counters recorded raw, latency excluded from any decision (M6); delta-scope restriction (M7); instrument sensitivity bracketed live by PC/NC (M8); MEASUREMENT_INVALID vs FALSIFIES precedence as in section 9 (M9); no-benchmark assertion in derived artifacts (M10).
- Missing/inapplicable fields: if any gate cannot be evaluated because a prerequisite vanished (e.g., server cannot start, git object missing, freeze hash mismatch), that is a measurement failure: status=MEASUREMENT_INVALID with the smallest unblocking action stated — never a negative scientific result.

## 11. Outcomes and consequences

- **Positive (POSITIVE, promote)**: verdict `promote_to_product=true`; delta ships to main via `product-promote.yml` after the workflow's own compileall/validate_repo/unittest gate; C-PARAM-INHERIT suggested update → `VALIDATED` (bounded statement: *shipped executable parameterized carrier + known-negative refusal certificate, demonstrated on the deterministic credential-free real-HTTP substrate; economics/model-agent benefit explicitly not claimed here*); B1 cleared; next eligible product work: B2 non-ceiling task-bank certificate using the shipped carrier; the four-arm benchmark remains unfunded until readiness conditions hold.
- **Negative (FALSIFIES)**: no promotion, `promote_to_product=false`, claim retained EXPERIMENTAL; the failing gate (F1…F4) names the smallest repair; do not re-ask the identical certificate.
- **Invalid (MEASUREMENT_INVALID)**: no promotion; exact blocker + smallest unblocking action; governance defects routed to the Global Research Director; prior raw evidence preserved for reclassification without re-running.

## 12. Anticipated objections and do-not-assume

- Do not read the refusal certificate as support-generalization: out-of-support identifiers/values are refused precisely because of the induced support grammars, and the substrate keeps held-out values inside them by frozen construction (`handoff.json.unknown[2]` of the parent).
- Do not read `model_calls=0`/`model_tokens=0` as measured zero-cost economics — no model was invoked; no endpoint cost is claimed.
- Do not read the held-out 0.0 set as novelty-0.75-scale generalization; the certificate bounds the claim to *new identifiers within the induced support on the same substrate*.
- Do not treat `src/spider/kernel.py`'s absence from `freeze_artifacts` as an unpinned deliverable: both ends of the delta are git-blob-pinned (cfec9866 → b15ed848) and the promotion delta is mechanically restricted to the allowed roots.
- Do not promote this packet's scaffolding (harness, probe scripts) — only the two-file code delta is promotion payload.

## 13. References

- `research/experiments/EXP-PRODUCT-38094123727/request.json` (mandate, base_sha, design_contract_version 2)
- `research/experiments/EXP-PRODUCT-38094123727/spec.json` (this experiment's frozen design surface)
- `research/experiments/EXP-PRODUCT-37989728440/handoff.json` + `harness/audited_spider/*` + `harness/substrate.py` + `harness/run_experiment.py`
- `research/experiments/EXP-PRODUCT-37989728440/result.json`, `audit.json` (B-LITERAL-KERNEL 0.0, PC-EXACT-REPLAY 20/20, counter-only corrections, freeze-gate defect)
- `research/portfolio/PROGRAM_AUDIT_2026-10-10.md` (B1/B2/B3), `codex/claim_state.json`, `research/claims/registry.json`, `research/lanes/registry.json`
- `.github/workflows/product-promote.yml`, `scripts/freeze_experiment.py`, `scripts/validate_design_review.py`, `scripts/validate_repo.py`
- `src/spider/kernel.py` (pre-install blob cfec9866) and carrier blob `b15ed848` (byte-identical vendored copy at the freeze artifact path)