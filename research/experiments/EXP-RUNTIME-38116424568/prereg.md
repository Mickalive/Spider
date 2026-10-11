# EXP-RUNTIME-38116424568 preregistration

DESIGN NOT YET FROZEN — this file becomes immutable when the deterministic freezer runs.

## 1. Identity and binding scope

- experiment_id: `EXP-RUNTIME-38116424568`
- lane: `runtime`
- claim_ids: `["C-MEAS-VALID"]` (no other claim; `C-RESIDUAL-NOVELTY` / `C-PARAM-INHERIT` are graph/product-owned and must not appear)
- director mandate: cycle `38115894614`, action CONTINUE, cognitive_reset true, parent_handoff_disposition SUPERSEDE (carry-forward of EXP-RUNTIME-37973247935 preserved four-way in spec.json `parent_handoff_continuity`; its `next_question` is NOT this experiment's question)
- dependencies honored: (a) EXP-PRODUCT-37989728440 bounded negative on the mandatory-discovery deterministic REST class — that class is NOT re-tested here, only cited as the ceiling reference; (b) pre-freeze arithmetic certificate for COLD/RETRIEVAL < 0.95 at novelty >= 0.5 and matched correctness >= 0.80, freeze nothing if unsatisfiable — computed below and verified by an executed rule-level simulation before this file is frozen; (c) the diagnosed runtime repairs (add hop-by-hop `Connection` to EXCLUDED_HEADERS; align capture-stability gate to the WAL byte vector per prereg section 8 of the parent) are recorded for future real-drift reuse and are NOT re-run this cycle.

Scope boundary: this packet certifies a MEASUREMENT SUBSTRATE (non-degenerate asymmetric-discovery task bank) usable under the C-MEAS-VALID VALIDATED bounded ceiling. It does not advance claim status, promotes nothing to Product, and does not claim any real-agent capability. Executors are deterministic benchmark stand-ins; real-agent economics are for the flagship B2 benchmark to measure on this bank.

## 2. Question and hypothesis

Question (binding, from mandate): on a credential-free substrate class materially different from the mandatory-discovery deterministic REST class — multi-task sessions where one-time session/resource/schema discovery is amortized or cached across tasks — can an asymmetric-discovery task bank be certified ARITHMETICALLY BEFORE FREEZE: B-COLD-RE-DERIVE and B-RETRIEVAL-SHAPED success_rate < 0.95 at novelty >= 0.5 on at least one task family, matched correctness >= 0.80 for all arms, a real treatment/comparator behavioural distinction, honest per-condition counters (http_requests + retrieval_calls + verification_calls + repair_attempts), and a preregistered contamination/dynamic-range certificate — deliverable as a reusable substrate unblocking the flagship inheritance benchmark B2; with the mandated escape clause that if the certificate is unsatisfiable on every credential-free substrate tested, the outcome is a bounded substrate-class negative and nothing is frozen.

Hypothesis: the SESSION-BINDING class (credential-free deterministic stdlib localhost HTTP; K=8-task sessions; one-time 48-bit session-scoped resource binding revealed exactly once in a workflow commit receipt and absent from every idempotent channel; server-enforced session/family scoping that rejects stale, foreign or consumed bindings) yields a bank certifiable pre-freeze with non-degenerate dynamic range: under the frozen benchmark conventions, each of two families (F1-RECORDS, F2-WIDGETS) has predicted success 0.875 (140/160) for both comparators at novelty 0.50 and 0.75 (inside [0.80, 0.95)), 1.0 below novelty 0.5, with T-AMORTIZED-DISCOVERY and PC-EXACT-REPLAY at 1.0, and with ≥ 2 of 3 counter dimensions behaviorally distinct between treatment and comparators.

## 3. Substrate construction (frozen literals)

- Transport: Python stdlib only (`http.server` / `urllib` / `http.client` / `hashlib` / `json`), single in-process server on 127.0.0.1, no persistence, no external network, no credentials, no LLM calls. EXECUTE may not import `research/runtime/*` or any other repo module into the measurement path (frozen prohibition).
- Sessions: K=8 tasks per session. `GET /api/v1/{family}/session` → `{session_token, schema, epoch}`; session_token is opaque (SHA-256 over server secret + family + novelty + session_index) and is NOT the binding seed.
- One-time binding: 48-bit value = SHA-256(server_secret, family, novelty, session_index, "binding") truncated to 48 bits; revealed EXACTLY ONCE in the commit receipt of the precursor task; absent from every idempotent channel (`/session`, `/task/{i}`, non-receipt commit responses, all 400/409 bodies) — mechanically scanned by NC-NO-LEAK; consumed on first successful use at the chain task; any stale/foreign/consumed value → 400.
- Chain placement: novelty 0.50 → precursor task index 4, chain task index 5 (carry distance 1); novelty 0.75 → precursor task index 5, chain task index 7 (carry distance 2). No chain task at novelty 0.00/0.25.
- Novelty bands and semantics: 0.00 → schema_required=false, resource_id explicit → no discovery needed; 0.25 → schema_required=true (schema via /session), resource_id explicit; 0.50 → schema + one chain task; 0.75 → schema + chain at distance 2 (requires >1-step context retention). Novelty = fraction of commit parameters not determined by (task spec ∪ frozen grammar): 0/4, 1/4, 2/4 (chain), 3/4 (chain). Certificate gates evaluate at novelty >= 0.5.
- Sampling: N_SESSIONS=20 per (family × novelty × arm) cell → 160 scored tasks/cell; families F1-RECORDS and F2-WIDGETS; scored arms T, B-COLD-RE-DERIVE, B-RETRIEVAL-SHAPED, PC-EXACT-REPLAY; full scored matrix 640 sessions; controls add ≈ 720 session-runs (see §7); double-run of the full scored matrix required.
- Determinism: single run_seed fixed at EXECUTE; per-(family,novelty,session_index) seeds via SHA-256(seed, family, novelty, session_index); no process `hash()`; no wall-clock dependence in outcomes (latency recorded advisory-only).
- Commits: `POST /api/v1/{family}/commit` with `{session_token, task_index, resource_id, payload}` → 200 + receipt on success; 400 invalid/missing/consumed binding; 409 already-committed (re-commit of the precursor NEVER re-reveals the binding).
- Scoring: pure stateless function over (task_index, final_committed_state) only; scorer never sees arm identity, arm traces, retrieval stores or counters (arm-blind contract). Ground truth = deterministic manifest generated from the seed. No synthetic/assistive values anywhere (no hints, no partial credit, exact-match only).

## 4. Arms and frozen policies

- T-AMORTIZED-DISCOVERY (treatment): GET /session once per session; retains context including the precursor commit receipt; captures next_resource_id (the binding) from the receipt; commits the chain task with the captured binding; one commit per task. Predicted: success 1.0; http=17; retrieval_calls=0; verification_calls=8; repair_attempts=0 per session.
- B-COLD-RE-DERIVE (mandated comparator): before EVERY task, GET /session and DISCARD prior task context (no receipt retention); at the chain task the binding is not re-derivable (one-time, 48-bit, non-leaked; ~2^47 guesses needed vs a 128-request/session budget); first commit → 400, one repair re-attempt → 400; chain task fails. Predicted: success 0.875 (7/8) at novelty >= 0.5, 1.0 below; http=25; retrieval_calls=0; verification_calls=9; repair_attempts=1 per session.
- B-RETRIEVAL-SHAPED (mandated comparator): identical request pattern to cold PLUS exactly one local retrieval_calls per task over the frozen prior-session store (8/session); at the chain task it retrieves a binding value recorded in a DIFFERENT session (stale within the current session's registry, server-enforced) → 400 → fail. Predicted: success 0.875 at novelty >= 0.5, 1.0 below; http=25; retrieval_calls=8; verification_calls=9; repair_attempts=1 per session.
- PC-EXACT-REPLAY (positive control): golden-input oracle given the exact session binding + schema by frozen construction (no HTTP discovery); proves substrate completability and non-degenerate scoring. Predicted: 1.0; http=17; retrieval_calls=0; verification_calls=8; repair_attempts=0.
- Arms interact ONLY through the HTTP surface; access to server-process state, bank files or generator internals is a protocol violation (frozen prohibition). The 128-request/session budget applies to all arms equally (NC-EQUAL-BUDGET) and never binds (max predicted usage 25).

## 5. Counters (honest per-condition accounting)

All four counters are re-derived from ONE interleaved execution trace with monotonic request ids (NC-COUNTER-INTEGRITY):
- http_requests = every HTTP request issued by the arm (success, failure, repair re-attempts);
- retrieval_calls = local retrieval invocations over the frozen prior-session store (B-RETRIEVAL-SHAPED only; 0 for all other arms);
- verification_calls = commit requests issued = ground-truth checks performed (includes repair re-attempts);
- repair_attempts = commit requests issued after an initial failure on the same task.

Frozen invariants: http_requests == session_creates + task_reads + commit_requests; verification_calls == commit_requests; repair_attempts <= verification_calls; retrieval_calls > 0 only for B-RETRIEVAL-SHAPED. Trace re-derivation must reproduce the reported counters exactly.

Predicted per-session vectors (probe-verified): T/PC = (17, 0, 8, 0); COLD = (25, 0, 9, 1); RETRIEVAL = (25, 8, 9, 1).

## 6. Pre-freeze arithmetic certificate (computed, not asserted)

Computation method: a pure-Python rule-level simulation of the frozen construction rules (no sockets, no bank, no treatment measurement) executed at DESIGN time. Probe: /tmp/opencode/exp38116424568/probe_arithmetic_certificate.py, sha256 556d3dafbf89ea24ab84dbe23bf33ff8354d0a3944a855b10d4a0f1cc663d0c7. Transport prerequisite verified separately: in-process stdlib HTTPServer on 127.0.0.1 answered urllib GET with HTTP 200 JSON (python3 3.12.15).

Predicted per-cell success (both families, 160 tasks/cell):
- novelty 0.00: T=1.0, COLD=1.0, RETRIEVAL=1.0, PC=1.0
- novelty 0.25: T=1.0, COLD=1.0, RETRIEVAL=1.0, PC=1.0
- novelty 0.50: T=1.0, PC=1.0; COLD=0.875 (140/160), RETRIEVAL=0.875 (140/160)
- novelty 0.75: T=1.0, PC=1.0; COLD=0.875 (140/160), RETRIEVAL=0.875 (140/160)

Gate evaluation: both families certify — COLD 0.875 < 0.95 and RETRIEVAL 0.875 < 0.95 at novelty 0.50 and 0.75; matched correctness min = 0.875 >= 0.80 for all arms; margins 0.075 below the ceiling and 0.075 above the floor.

Behavioral distinction (frozen numeric profile): success margin T−COLD = T−RETRIEVAL = 0.125 >= 1/K at novelty >= 0.5; counter dims: http 17 < 25 = 25 (distinct), retrieval 8 > 0 = 0 (distinct), repair 1 = 1 > 0 (distinct) → 3/3 dims, rule requires >= 2.

Control predictions (probe-verified): PC = 1.0; NC-EMPTIED-CONTEXT = 0.875; NC-SHUFFLED-BINDING = 0.875; NC-FAMILY-ISOLATION = 0.875; NC-NO-DISCOVERY-DIRECT = 1.0 at novelty 0.00, 0.0 at >= 0.25; NC-MECHANISM-OFF → COLD = RETRIEVAL = 1.0 → certificate FALSE (negative branch inhabited: the certificate procedure demonstrably fires negative on a degenerate configuration, proving it is non-vacuous and that the one-time mechanism — not bank content or arm definitions alone — produces the range).

Novelty monotonicity is NOT preregistered: identical 0.875 at bands 0.50 and 0.75 is expected by construction (the same one-time-binding failure mechanism at both carry distances). No monotonicity gate exists in the decision rule.

## 7. Controls (stable identities, expected values)

- PC-EXACT-REPLAY → 1.0 all bands (positive control: substrate completable; also T-liveness anchor — T must equal PC; a broken capture loop drops T to 0.875 and trips the distinction gate, so SUPPORTS cannot be claimed with a dead treatment).
- NC-MECHANISM-OFF → certificate FALSE (null control / mechanism ablation: binding also exposed in /session; identical bank and arms; comparators reach 1.0).
- NC-EMPTIED-CONTEXT → 0.875 at novelty >= 0.5, 1.0 below (T minus retention; isolates retention as the operative T property).
- NC-SHUFFLED-BINDING → 0.875 at novelty >= 0.5 (T with another session's binding; server rejects → session scoping is server-enforced).
- NC-FAMILY-ISOLATION → 0.875 at novelty >= 0.5 (T with the other family's binding; server rejects).
- NC-NO-DISCOVERY-DIRECT → 1.0 at 0.00, 0.0 at >= 0.25 (spec-only actor; proves discovery is genuinely required).
- NC-NO-LEAK → binding (and any reconstructing value) absent from every idempotent channel; entropy recomputed >= 40 bits (actual 48). Any hit → F-LEAK.
- NC-EQUAL-BUDGET → same 128-request ceiling for all arms; budget never binds.
- NC-NO-SYNTHETIC → no hints/partial credit; exact-match scoring.
- NC-ARM-BLIND-SCORING → scorer sees (task_index, final_committed_state) only.
- NC-COUNTER-INTEGRITY → invariants of §5 re-derived from the single trace.
- NC-DOUBLE-RUN → full scored matrix twice with same run_seed; byte-identical outcomes and counters required.

Control sample sizes: 20 sessions per control cell (same as scored cells); NC-FAMILY-ISOLATION runs the two high-novelty bands on both families (80 sessions); all other controls run the full (family × novelty) grid (160 sessions each).

## 8. Contamination and dynamic-range certificate (preregistered)

- Cache/context contents: T's retained context contains only {session schema, explicit specs-derived ids, the current session's receipt}; B-RETRIEVAL-SHAPED's store contains only values from OTHER sessions (frozen prior-session store); no arm ever receives the current session's binding except via the single server-issued receipt.
- Server-enforced: resource_id validation against the live session registry; binding consumed on first use; stale/foreign/consumed → 400 (verified by NC-SHUFFLED-BINDING, NC-FAMILY-ISOLATION, NC-NO-LEAK).
- Matched manifests: identical task manifests per (family, novelty) across ALL arms; arms differ only in frozen policy, never in stimuli.
- Cache-only oracle: a spec-only / store-only actor completes 0 tasks at novelty >= 0.25 (behavioral proxy: NC-NO-DISCOVERY-DIRECT); no test-session answer is obtainable from stores.
- Dynamic-range certificate (the mandate's): B-COLD-RE-DERIVE and B-RETRIEVAL-SHAPED success_rate < 0.95 at novelty >= 0.5 on at least one family, with matched correctness >= 0.80 for all arms — certified arithmetically before freeze (§6) and verified at measure time by the expected-outcome equality gate (the realized rates must equal the frozen expected vectors, else MEASUREMENT_INVALID).

## 9. Measurement validity and integrity gates

Validity class: deterministic closed-form measurement over a construction-derived bank; no stochasticity, no LLM, no external network. Status is COMPLETE only when every gate below passes; otherwise the packet is MEASUREMENT_INVALID (infrastructure/validity) or MIXED/FALSIFIES (scientific, per §10).

Gates: (G1) expected-vs-measured equality on every scored cell (per-task outcomes + per-cell counter vectors) — ANY deviation, including a non-chain cell failing, → MEASUREMENT_INVALID; (G2) NC-DOUBLE-RUN byte-identical; (G3) NC-NO-LEAK clean and entropy >= 40 bits; (G4) NC-COUNTER-INTEGRITY trace re-derivation; (G5) NC-ARM-BLIND-SCORING interface contract honored; (G6) frozen files untouched; stdlib-only measurement path; no arm protocol violation.

Infrastructure or substrate failure is NEVER encoded as scientific falsification: it maps to MEASUREMENT_INVALID with the smallest unblocking next action, per failure discipline.

## 10. Decision rule (frozen mapping)

- SUPPORTS: ≥ 1 family certifies (COLD < 0.95 AND RETRIEVAL < 0.95 at novelty in {0.50, 0.75}) AND matched correctness ≥ 0.80 for ALL arms at ALL bands AND behavioral distinction holds (≥ 2 of 3 counter dims distinct AND success margins T−COLD ≥ 1/8 AND T−RETRIEVAL ≥ 1/8 at novelty ≥ 0.5) AND all control predictions hold (PC=1.0; NC-EMPTIED-CONTEXT=0.875; NC-SHUFFLED-BINDING=0.875; NC-FAMILY-ISOLATION=0.875; NC-NO-DISCOVERY-DIRECT 1.0/0.0; NC-MECHANISM-OFF → FALSE) AND gates G1–G6 pass → deliver the certified bank (task manifests, stdlib HTTP protocol, executor policy definitions, scored evidence, contamination certificate) as reusable substrate for the B2 benchmark; C-MEAS-VALID substrate-validity evidence; no claim status change, no promotion.
- FALSIFIES: zero families certify (comparators ≥ 0.95 at novelty ≥ 0.5 in BOTH families, or any arm < 0.80), with gates G1–G6 passed → bounded substrate-class negative: SESSION-BINDING (one-time session-scoped discovery on credential-free stdlib deterministic substrates) is closed; flag the Global Director that the flagship benchmark class requires credentialed substrates or a changed product thesis. This is the mandate's stated honest decision-changing outcome; nothing is frozen when unsatisfiable (escape clause).
- MIXED: ≥ 1 family achieves range but integrity/control expectations fail (e.g., NC-NO-LEAK fires → F-LEAK; counter inconsistency; mechanism-off fails to produce FALSE; exactly one family certifies while the other fails) → bank is NOT deliverable as certified; emit the exact repair list.
- MEASUREMENT_INVALID: any of G1–G6 fails (infrastructure, nondeterminism, mismatch, frozen-file modification, protocol violation) → no scientific reading; record diagnosis + smallest unblocking next action.

## 11. Consequences

Positive: the flagship inheritance benchmark B2 — the program's verified blocker "benchmark degeneracy: cold/retrieval at the 1.0 ceiling" — is unblocked by a certified, credential-free, deterministic, zero-model-cost bank with off-ceiling comparators (0.875), an on-ceiling amortized inheritor (1.0), strictly lower treatment counter costs (http 17 < 25, repair 0 < 1, retr 0 < 8), and a mechanically verified contamination certificate.

Negative: a bounded substrate-class negative is recorded for the credential-free one-time-session class, turning "B2 blocked" into "B2 class closed on this substrate family" and forcing the credentialed-substrate or thesis-change decision — the honest decision-changing outcome the mandate requires — while preserving the freeze-nothing escape clause for any unsatisfiable variant.

## 12. EXECUTE instructions (frozen)

- Author the bank generator, server, executors, scorer and counter extractor from the literals in this file and spec.json; stdlib only; record every source file path + SHA-256 in result.json.artifacts.
- Fix run_seed at run start and record it in provenance.json; run the full scored matrix; run all controls; run the double-run; run NC-NO-LEAK scans and entropy recomputation.
- Emit result.json (status/outcome per §10), report.md, provenance.json (GitHub run id, seed, environment, artifact hashes, exact commands). Preserve RAW EVIDENCE (server access log with monotonic request ids, per-session traces, per-task outcomes) separate from DERIVED MEASUREMENTS (cell rates, counter totals) and from INTERPRETATION (report.md within frozen bounds).
- Do not modify request.json, spec.json, prereg.md or freeze.json; do not re-run the excluded REST class; do not run the superseded parent question.