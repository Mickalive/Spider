# EXP-RUNTIME-38121196004 preregistration

This file becomes immutable when the deterministic freezer (`scripts/freeze_experiment.py`) writes `freeze.json`.

## 1. Identity and binding scope

- experiment_id: `EXP-RUNTIME-38121196004`
- lane: `runtime`
- claim_ids: `["C-MEAS-VALID"]` (no other claim; `C-RESIDUAL-NOVELTY` / `C-PARAM-INHERIT` / `C-LLM-INHERIT` are not runtime-charter claims and MUST NOT appear)
- director mandate: cycle `38120577942`, action CONTINUE, cognitive_reset true, `parent_handoff_disposition = SUPERSEDE`. The binding mandate question is `request.json:director_mandate.allocation.question`; its target claim is C-MEAS-VALID. The four-way carry-forward of the superseded parent `EXP-RUNTIME-37973247935` is preserved in `spec.json:parent_handoff_continuity`, and the parent `next_question` (fingerprint repair + out-of-surface re-run) is explicitly NOT this experiment's question.
- Dependencies honored: (a) `EXP-PRODUCT-37989728440` bounded negative on the mandatory-discovery deterministic REST class is cited as the off-class ceiling reference and is NOT re-tested (a fourth re-run is explicitly excluded); (b) a pre-freeze arithmetic certificate for comparator success < 0.95 at novelty >= 0.5 and matched arm correctness >= 0.80, freeze nothing if unsatisfiable; (c) the parked runtime out-of-surface oracle repair (add hop-by-hop `Connection` to the excluded headers, align the capture-stability gate to the WAL-byte vector, re-implement M-REVERT-LOGICAL as a compensating-inverse logical restore) is recorded for future real-drift use only and is NOT run here.

Scope boundary: this packet certifies a MEASUREMENT SUBSTRATE (a non-degenerate asymmetric-discovery task bank) usable under C-MEAS-VALID's bounded scope. It does not advance claim status, promotes nothing to Product, and claims no real-agent capability. Executors are deterministic benchmark stand-ins; real-agent economics are for the flagship B2 benchmark to measure on this bank.

## 2. Question and hypothesis

Question (binding, from mandate): on a credential-free substrate class materially different from the mandatory-discovery deterministic REST class - multi-task sessions where one-time session/resource/schema discovery is amortized or cached across tasks - can an asymmetric-discovery task bank be certified ARITHMETICALLY BEFORE FREEZE (B-COLD-RE-DERIVE and B-RETRIEVAL-SHAPED success_rate < 0.95 at novelty >= 0.5 on at least one family; matched correctness >= 0.80 for all arms; a real treatment/comparator behavioural distinction; honest per-condition counters `http_requests + retrieval_calls + verification_calls + repair_attempts`; and a preregistered contamination/dynamic-range certificate) so that the bank is deliverable as a reusable substrate unblocking the flagship inheritance benchmark B2? If the certificate is unsatisfiable on every credential-free substrate tested, the mandated outcome is a bounded substrate-class negative and nothing is frozen.

Hypothesis: the SESSION-BINDING-AMORTIZED class yields a non-degenerate bank. Under the frozen benchmark conventions, each of F1-RECORDS and F2-WIDGETS has predicted comparator success_rate 0.875 (140/160) at novelty 0.50 and 0.75 - strictly below the 0.95 ceiling and above the 0.80 floor - and 1.0 at novelty 0.00/0.25, while T-AMORTIZED-DISCOVERY and PC-EXACT-REPLAY reach 1.0 at every band, with at least two of the three counter dimensions behaviourally distinct between treatment and comparators.

## 3. Substrate construction (frozen literals)

- Transport: Python stdlib only (`http.server` / `http.client` / `urllib` / `hashlib` / `json`), a single in-process server bound to `127.0.0.1`, no persistence, no external network, no credentials, no LLM calls. EXECUTE MUST NOT import `research/runtime/*.py` or any other repository module into the measurement path (frozen prohibition).
- Sessions: K=8 tasks per session. `GET /api/v1/{family}/session` -> `{session_token, schema, epoch}`; `session_token` is opaque (SHA-256 over server secret + family + novelty + session_index) and is NOT the binding seed.
- One-time binding: a 48-bit value `= SHA-256(server_secret, family, novelty, session_index, "binding")` truncated to 48 bits. It is revealed EXACTLY ONCE in the precursor task's commit receipt, is absent from every idempotent channel (`/session`, `/task/{i}`, non-receipt commit responses, all 400/409 bodies - mechanically scanned by NC-NO-LEAK), is consumed on first successful use, and any stale/foreign/consumed value is rejected with 400. Re-commit of the precursor returns 409 and NEVER re-reveals the binding.
- Chain placement: novelty 0.50 -> precursor task index 4, chain task index 5 (carry distance 1); novelty 0.75 -> precursor task index 5, chain task index 7 (carry distance 2). No chain task at novelty 0.00/0.25.
- Novelty bands: 0.00 = schema not required, resource_id explicit, no discovery; 0.25 = schema required (discovered via /session), resource_id explicit; 0.50 = schema + one chain task (distance 1); 0.75 = schema + chain task (distance 2, requires more than one step of context retention). Novelty is the fraction of commit parameters not determined by (task spec union frozen grammar): 0/4, 1/4, 2/4 chain, 3/4 chain. Certificate gates evaluate at novelty >= 0.5.
- Sampling: N_SESSIONS=20 per (family x novelty x scored arm) cell -> 160 tasks per cell; families F1-RECORDS and F2-WIDGETS; scored arms T-AMORTIZED-DISCOVERY, B-COLD-RE-DERIVE, B-RETRIEVAL-SHAPED, PC-EXACT-REPLAY; 640 scored sessions total; controls add the cells in section 7; a full double-run is required.
- Determinism: one `run_seed` fixed at EXECUTE; per-(family, novelty, session_index) seeds via `SHA-256(seed, family, novelty, session_index)`; no process `hash()`; no wall-clock dependence in outcomes (latency is advisory only).
- Commits: `POST /api/v1/{family}/commit` with `{session_token, task_index, resource_id, payload}` -> 200 + receipt on success; 400 invalid/missing/consumed binding; 409 already-committed.
- Scoring: a pure stateless function over `(task_index, final_committed_state)` only; the scorer never sees arm identity, traces, retrieval stores or counters (arm-blind contract). Ground truth is a deterministic manifest generated from the seed. No synthetic or assistive values (no hints, no partial credit, exact match only).

## 4. Arms and frozen policies

- T-AMORTIZED-DISCOVERY (treatment): GET /session once per session; retain context including the precursor commit receipt; capture `next_resource_id` (the binding) from the receipt; commit each task once, using the captured binding at the chain task. Predicted success 1.0 all bands; per-session http=17, retrieval_calls=0, verification_calls=8, repair_attempts=0.
- B-COLD-RE-DERIVE (mandated comparator): before EVERY task, GET /session and DISCARD prior task context (no receipt retention); at the chain task the binding is not re-derivable (one-time, 48-bit, non-leaked; roughly 2^47 guesses against a 128-request/session budget); the first commit returns 400 and one repair re-attempt also returns 400, so the chain task fails. Predicted success 0.875 (7/8) at novelty >= 0.5 and 1.0 below; per-session http=25 (24 at novelty 0.00/0.25), retrieval_calls=0, verification_calls=9 (8 at 0.00/0.25), repair_attempts=1 (0 at 0.00/0.25).
- B-RETRIEVAL-SHAPED (mandated comparator): the same request pattern as cold PLUS exactly one local retrieval_call per task over the frozen prior-session store (8/session); at the chain task it retrieves a binding recorded in a DIFFERENT session (stale within the current session's registry, server-enforced) -> 400 -> fail. Predicted success 0.875 at novelty >= 0.5 and 1.0 below; per-session http=25 (24 at 0.00/0.25), retrieval_calls=8, verification_calls=9 (8 at 0.00/0.25), repair_attempts=1 (0 at 0.00/0.25).
- PC-EXACT-REPLAY (positive control): a golden-input executor given the session's exact binding and schema by frozen construction (no HTTP discovery); it proves the substrate is completable and the scorer non-degenerate. Predicted success 1.0 all bands; per-session http=17, retrieval_calls=0, verification_calls=8, repair_attempts=0.
- Arms interact ONLY through the HTTP surface; access to server-process state, bank files or generator internals is a frozen protocol violation. The 128-request/session budget applies to all arms equally (NC-EQUAL-BUDGET) and never binds (max predicted usage 25).

## 5. Counters (honest per-condition accounting)

All four counters are re-derived from ONE interleaved execution trace with monotonic request ids (NC-COUNTER-INTEGRITY):
- `http_requests`: every HTTP request issued by the arm (success, failure, repair re-attempts);
- `retrieval_calls`: local retrieval invocations over the frozen prior-session store (B-RETRIEVAL-SHAPED only; 0 for all other arms);
- `verification_calls`: commit requests issued = ground-truth checks performed (includes repair re-attempts);
- `repair_attempts`: commit requests issued after an initial failure on the same task.

Frozen invariants: `http_requests == session_gets + task_reads + commit_requests`; `verification_calls == commit_requests`; `repair_attempts <= verification_calls`; `retrieval_calls > 0` only for B-RETRIEVAL-SHAPED. Trace re-derivation must reproduce the reported counters exactly.

Predicted per-session vectors (probe-verified), band-specific: T/PC all bands = (http 17, retr 0, verif 8, repair 0); COLD novelty 0.00/0.25 = (24, 0, 8, 0), novelty 0.50/0.75 = (25, 0, 9, 1); RETRIEVAL novelty 0.00/0.25 = (24, 8, 8, 0), novelty 0.50/0.75 = (25, 8, 9, 1).

## 6. Pre-freeze arithmetic certificate (computed, not asserted)

Computation method: a pure-Python rule-level simulation of the frozen construction and arm policies (no bank, no treatment measurement) executed at DESIGN time, plus a real stdlib HTTP transport probe. Probe: `/tmp/opencode/exp38121196004/probe_certificate.py`, sha256 `f36dd4bdc0766361dbeb5668617936306b8aa209cf75eef3a0ee70113d997039`; probe output self-hash `17bbf7d0b9b5f0beea143c5ef34b4c11637a1fca46fad87c4ca40753ed2c8175`. The probe is DESIGN-time ephemeral and is NOT an interpretation dependency: the arithmetic below is frozen here and in `spec.json` and re-derivable from those literals.

Transport prerequisite (separate live probe, python3 3.12.15): an in-process stdlib HTTPServer on 127.0.0.1 answered `GET /session` with HTTP 200 JSON, `GET /task/5` with 200, `POST commit` with the valid binding with 200, a repeated POST with the same consumed binding with 409, and a POST with a wrong binding with 400.

Predicted per-cell success (both families, 160 tasks per cell):
- novelty 0.00: T=1.0, COLD=1.0, RETRIEVAL=1.0, PC=1.0
- novelty 0.25: T=1.0, COLD=1.0, RETRIEVAL=1.0, PC=1.0
- novelty 0.50: T=1.0, PC=1.0; COLD=0.875 (140/160), RETRIEVAL=0.875 (140/160)
- novelty 0.75: T=1.0, PC=1.0; COLD=0.875 (140/160), RETRIEVAL=0.875 (140/160)

Gate evaluation: both families certify - COLD 0.875 < 0.95 and RETRIEVAL 0.875 < 0.95 at novelty 0.50 and 0.75; minimum arm correctness 0.875 >= 0.80; margins 0.075 below the ceiling and 0.075 above the floor.

Behavioural distinction (frozen numeric profile): success margins T-COLD = T-RETRIEVAL = 0.125 >= 1/K at novelty >= 0.5; counter dimensions http 17 < 25 (distinct), retrieval 0 < 8 (distinct), repair 0 < 1 (distinct) -> 3/3 dimensions, rule requires at least 2.

Control predictions (probe-verified): PC = 1.0; NC-EMPTIED-CONTEXT = 0.875; NC-SHUFFLED-BINDING = 0.875; NC-FAMILY-ISOLATION = 0.875; NC-NO-DISCOVERY-DIRECT = 1.0 at novelty 0.00 and 0.0 at novelty >= 0.25; NC-MECHANISM-OFF -> COLD = RETRIEVAL = 1.0 -> certificate FALSE (the negative branch is inhabited: the certificate procedure demonstrably fires negative on a degenerate configuration, proving it is non-vacuous and that the one-time mechanism - not the bank content or the arm definitions alone - produces the range).

Novelty monotonicity is NOT preregistered and NOT gated: identical 0.875 at bands 0.50 and 0.75 is expected by construction (the same one-time-binding failure mechanism at both carry distances).

## 7. Controls (stable identities, expected values)

- PC-EXACT-REPLAY -> 1.0 all bands (positive control: substrate completable; also the T-liveness anchor - T must equal PC, and a broken capture loop drops T and trips the distinction gate, so SUPPORTS cannot be claimed with a dead treatment).
- NC-MECHANISM-OFF -> certificate FALSE (null control / mechanism ablation: the binding is also exposed by `/session`, so the comparators reach 1.0 with the identical bank and arms).
- NC-EMPTIED-CONTEXT -> 0.875 at novelty >= 0.5, 1.0 below (T minus retention; isolates retention as the operative T property).
- NC-SHUFFLED-BINDING -> 0.875 at novelty >= 0.5 (T with another session's binding; the server rejects it, so session-scoping is server-enforced).
- NC-FAMILY-ISOLATION -> 0.875 at novelty >= 0.5 (T with the other family's binding; the server rejects it).
- NC-NO-DISCOVERY-DIRECT -> 1.0 at novelty 0.00, 0.0 at novelty >= 0.25 (spec-only actor; proves discovery is genuinely required).
- NC-NO-LEAK -> the binding (and any value sufficient to reconstruct it) is absent from every idempotent channel; recomputed entropy >= 40 bits (actual 48). A single hit -> F-LEAK -> MIXED.
- NC-EQUAL-BUDGET -> the same 128-request ceiling for all arms; the budget never binds.
- NC-NO-SYNTHETIC -> no hints or partial credit; exact-match scoring.
- NC-ARM-BLIND-SCORING -> the scorer sees only `(task_index, final_committed_state)`.
- NC-COUNTER-INTEGRITY -> the section-5 invariants re-derived from the single trace.
- NC-DOUBLE-RUN -> the full scored matrix is run twice with the same run_seed; outcomes and counters must be byte-identical.

Control sample sizes: 20 sessions per control cell (same as scored cells); NC-FAMILY-ISOLATION runs the two high-novelty bands on both families (80 sessions); all other controls run the full (family x novelty) grid (160 sessions each).

## 8. Contamination and dynamic-range certificate (preregistered)

- Cache/context contents: T's retained context contains only {session schema, explicit spec-derived ids, the current session's receipt}; B-RETRIEVAL-SHAPED's store contains only values from OTHER sessions (frozen prior-session store); no arm receives the current session's binding except through the single server-issued receipt.
- Server-enforced: the server validates every resource_id against the live session registry and consumes the binding on first use; stale/foreign/consumed -> 400 (verified by NC-SHUFFLED-BINDING, NC-FAMILY-ISOLATION, NC-NO-LEAK).
- Matched manifests: identical task manifests per (family, novelty) across ALL arms; arms differ only in frozen policy, never in stimuli.
- Cache-only oracle: a spec-only / store-only actor completes 0 tasks at novelty >= 0.25 (behavioural proxy NC-NO-DISCOVERY-DIRECT); no test-session answer is obtainable from any store.
- Dynamic-range certificate (the mandate's): B-COLD-RE-DERIVE and B-RETRIEVAL-SHAPED success_rate < 0.95 at novelty >= 0.5 on at least one family, with matched correctness >= 0.80 for all arms - certified arithmetically before freeze (section 6) and evaluated at measure time from the scored rates by the section-10 decision rule.

## 9. Measurement validity and integrity gates

Validity class: a deterministic closed-form construction measurement over a frozen-literal bank; no stochasticity, no LLM, no external network.

Two gate classes are deliberately separated:
- VALIDITY GATES V1-V7 decide whether the measurement is interpretable at all: (V1) packet immutability and stdlib-only measurement path; (V2) NC-DOUBLE-RUN byte-identical outcomes and counters; (V3) NC-NO-LEAK clean and entropy recomputed >= 40 bits; (V4) NC-COUNTER-INTEGRITY trace re-derivation matches; (V5) NC-ARM-BLIND-SCORING interface contract honored; (V6) matched manifests across arms and no arm protocol violation; (V7) NC-SHUFFLED-BINDING and NC-FAMILY-ISOLATION confirm server-enforced session/family scope and binding consumption.
- SCIENTIFIC RATE MEASUREMENTS (the per-cell arm success rates) are genuine measured outputs. They are NOT equality-frozen: a measured rate that differs from the section-6 prediction is evaluated by the decision rule and is NEVER auto-classified as invalid, unless it co-occurs with a V1-V7 failure.

Infrastructure or substrate failure is NEVER encoded as scientific falsification; it maps to MEASUREMENT_INVALID with the smallest unblocking next action.

## 10. Decision rule (frozen mapping)

A family certifies iff, at novelty >= 0.50, B-COLD-RE-DERIVE < 0.95 AND B-RETRIEVAL-SHAPED < 0.95, AND every scored arm (T, COLD, RETRIEVAL, PC) has success_rate >= 0.80 at every band, AND behavioural distinction holds (at least 2 of 3 counter dimensions distinct between T and each comparator AND success margins T-COLD >= 1/8 and T-RETRIEVAL >= 1/8 at novelty >= 0.5).

- SUPPORTS: at least one family certifies AND all controls equal their predicted values (PC=1.0; NC-EMPTIED-CONTEXT=0.875; NC-SHUFFLED-BINDING=0.875; NC-FAMILY-ISOLATION=0.875; NC-NO-DISCOVERY-DIRECT 1.0/0.0; NC-MECHANISM-OFF -> FALSE) AND validity gates V1-V7 pass -> deliver the certified bank (manifests, stdlib HTTP protocol, executor policy definitions, scored evidence, contamination certificate) as a reusable substrate for B2. C-MEAS-VALID substrate-validity evidence only; no status change; no promotion.
- FALSIFIES: zero families certify AND the non-certification is comparator-attributable (in BOTH families either a comparator success_rate >= 0.95 at novelty >= 0.5, i.e. the certificate is unsatisfiable on the frozen class, or a comparator success_rate < 0.80 at some band), with validity gates V1-V7 passed AND every control at its predicted value -> bounded substrate-class negative: the SESSION-BINDING-AMORTIZED class is closed for credential-free stdlib deterministic substrates -> flag the Global Director that the flagship benchmark class requires credentialed substrates or a changed product thesis. Reachability witness: the pre-registered NC-MECHANISM-OFF configuration ablates ONLY the one-time mechanism from the identical substrate, bank and arm policies, and under the frozen certificate returns unsatisfiable (comparators 1.0 >= 0.95 -> FALSE), so the negative branch is demonstrably inhabited and the procedure is non-vacuous; any realized degeneration of the mechanism-intact frozen class (comparators at/above ceiling) triggers this same branch at measure time.
- MIXED: validity gates V1-V7 pass and the classification is neither SUPPORTS nor FALSIFIES - exactly one family certifies while the other fails (partial dynamic range); OR a treatment-side failure (T < 0.80 or PC < 1.0) makes the bank undeliverable without closing the substrate class; OR a control does not equal its predicted value (NC-NO-LEAK fires -> F-LEAK, or NC-MECHANISM-OFF fails to flip to FALSE) -> the bank is not deliverable as certified; emit the exact repair list.
- MEASUREMENT_INVALID: any validity gate V1-V7 fails (infrastructure, nondeterminism, counter inconsistency, frozen-file modification, protocol violation, stdlib-only breach, matched-manifest mismatch, server-enforcement failure) -> no scientific reading; record the diagnosis and the smallest unblocking next action.

## 11. Consequences

Positive: the flagship inheritance benchmark B2 - currently gated on the verified blocker "benchmark degeneracy: cold/retrieval at the 1.0 ceiling" - is unblocked by a certified, credential-free, deterministic, zero-model-cost bank with off-ceiling comparators (0.875), an on-ceiling amortized inheritor (1.0), strictly lower treatment counter costs (http 17 < 25, repair 0 < 1, retrieval 0 < 8), and a mechanically verified contamination certificate.

Negative: a bounded substrate-class negative is recorded for the credential-free one-time-session class, turning "B2 blocked" into "B2 class closed on this substrate family" and forcing the credentialed-substrate or thesis-change decision - the honest decision-changing outcome the mandate requires - while preserving the freeze-nothing escape clause for any unsatisfiable variant.

## 12. EXECUTE instructions (frozen)

- Author the bank generator, server, executors, scorer and counter extractor from the literals in this file and `spec.json`; stdlib only; record every source file path plus SHA-256 in `result.json.artifacts`.
- Fix `run_seed` at run start and record it in `provenance.json`; run the full scored matrix, all controls, the double-run, the NC-NO-LEAK scans and the entropy recomputation.
- Emit `result.json` (status/outcome per section 10), `report.md`, `provenance.json` (GitHub run id, seed, environment, artifact hashes, exact commands). Keep RAW EVIDENCE (server access log with monotonic request ids, per-session traces, per-task outcomes) separate from DERIVED MEASUREMENTS (cell rates, counter totals) and from INTERPRETATION (`report.md` within the frozen bounds).
- Do not modify `request.json`, `spec.json`, `prereg.md` or `freeze.json`; do not re-run the excluded REST class; do not run the superseded parent question; do not import `research/runtime/*.py` or any other repository module into the measurement path.
