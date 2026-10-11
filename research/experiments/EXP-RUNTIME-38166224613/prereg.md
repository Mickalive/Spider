# Preregistration: EXP-RUNTIME-38166224613

Experiment ID: EXP-RUNTIME-38166224613
Lane: runtime
Design contract version: 2
Claim: C-MEAS-VALID (substrate validity only; no claim-status change, no promotion)
Stage: DESIGN (this file is frozen by `scripts/freeze_experiment.py`; execution follows only after `design_review.json` PASSes)

## 0. Authority and non-duplication

- Binding direction is the Director mandate in `request.json` (`cycle_id 38165620031`, action
  CONTINUE, claim `C-MEAS-VALID`, `cognitive_reset=true`, `parent_handoff_disposition=SUPERSEDE`).
- The parent handoff `EXP-RUNTIME-37973247935` (handoff sha256
  `984049809ebf393e805f59c9b8d083caf2ebfc387348079b06ccacbe41b8928e`) is SUPERSEDED and used only
  as continuity evidence. Its `next_question` (composite-oracle fingerprint repair) is NOT the target
  here.
- Pre-2.0 status is `NO_MATCH` for a pre-freeze dynamic-range certificate. The compact P2-WP003
  leakage precedent is the binding guard (see NC-NO-LEAK). Pre-2.0 runtime work concerned substrate
  demand and maintenance economics, not task-bank dynamic range.
- This experiment is NOT the bounded-negative mandatory-discovery deterministic REST class examined
  in `EXP-PRODUCT-37989728440` (where COLD and RETRIEVAL both sat at the 1.0 ceiling). It tests a
  materially different, credential-free ASYMMETRIC-discovery construction.
- Same-mandate Runtime predecessors `EXP-RUNTIME-38151074771` and `EXP-RUNTIME-38164599133` produced
  substantively complete designs whose only recorded failure was the shared independent
  design-review model outage (`opencode/exo-free`, exit 1, category substantive), not a scientific
  defect. This packet rigorously replicates the converged SESSION-BINDING-AMORTIZED construction at
  the new id, but is leaner, is fully self-contained (embedded satisfiability probe), repairs the
  comparator-identity framing, and explicitly discloses the amortization boundary (NC-MEMORYFUL).

## 1. Scientific question

Can a credential-free task bank engineered for ASYMMETRIC discovery - multi-task sessions in which
one-time session / resource / schema discovery is amortized or cached across tasks, and therefore
materially different from the bounded-negative mandatory-discovery deterministic REST class -
receive a PRE-FREEZE, arithmetically checkable dynamic-range certificate: B-COLD-RE-DERIVE and
B-RETRIEVAL-SHAPED success_rate < 0.95 at novelty >= 0.50 on at least one family, matched
correctness >= 0.80 for all arms, and a treatment/comparator distinction - so that it can serve as
the reusable substrate unblocking the flagship inheritance benchmark (B2), recording a bounded
substrate-class negative and freezing nothing if the certificate is unsatisfiable on every
credential-free substrate tested?

## 2. Hypothesis

At least one credential-free asymmetric-discovery family (class `SBA-CREDENTIAL-FREE-V1`) yields, at
novelty >= 0.50, B-COLD-RE-DERIVE and B-RETRIEVAL-SHAPED success_rate below the 0.95 ceiling -
specifically the closed form `(K-1)/K = 0.875` for `K = 8`, because exactly one of `K` tasks per
session (the chain task) is satisfiable only via the one-time session binding - while every scored
arm retains matched correctness >= 0.80 and the treatment `T-AMORTIZED-DISCOVERY` is behaviourally
and arithmetically distinct from both comparators.

## 3. Falsifier

Zero of the tested credential-free asymmetric-discovery families satisfy the certificate at
novelty >= 0.50 with all validity gates V1-V7 passing: in every family a comparator success_rate
>= 0.95, or comparator success is not distinguishable from T, or matched correctness < 0.80 for some
arm, or the mechanism-off control does not destroy the certificate. That is a bounded
substrate-class negative.

## 4. Substrate class `SBA-CREDENTIAL-FREE-V1`

- Families: `F1-RECORDS`, `F2-WIDGETS` (two independent families as required).
- `K = 8` tasks per session; novelty ladder `[0.00, 0.25, 0.50, 0.75]`; scored band `novelty >= 0.50`;
  20 sessions per cell -> 160 scored sessions.
- Credential-free, deterministic, stdlib only (`http.server.ThreadingHTTPServer` on 127.0.0.1 +
  `urllib.request`). `run_seed = SPIDER-RUNTIME-SBA-2026`; `server_secret =
  sha256(run_seed|"server_secret")[:32]`; no `secrets`, no clock, no `os.urandom`.
- Protocols:
  - `GET /api/v1/{family}/session` -> `{session_token, schema_epoch, epoch}`; NEVER contains the binding.
  - `GET /api/v1/{family}/task/{i}` -> `{index, requires_schema, resource_id, is_chain}`; the chain
    task's `resource_id` is null.
  - `POST /api/v1/{family}/commit` -> `200` receipt | `400` (bad_session / bad_index /
    schema_required / bad_resource) | `409` already_committed.
- One-time 48-bit session binding: `binding =
  sha256(secret|family|novelty|session_index|"binding")[:12]`. It is revealed exactly once, inside
  the FIRST successful commit receipt of the precursor task (`chain_resource_id`); a re-commit
  returns `409` with no re-reveal; the binding is consumed on the first successful chain commit and
  a wrong/foreign/consumed binding returns `400` with no binding echoed.
- Chain/precursor indices: at novelty `0.50`, precursor `4`, chain `5`; at novelty `0.75`, precursor
  `5`, chain `7`. `requires_schema = novelty >= 0.25`.

## 5. Arms, baselines and controls

Arms (matched counters `http_calls`, `retrieval_calls`, `verification_calls`, `repair_calls`):

- `T-AMORTIZED-DISCOVERY` (treatment): one session GET, retain receipts, capture the one-time
  binding from the precursor receipt, commit each task once. Predicted `1.0`; counters
  `(17, 0, 8, 0)`.
- `B-COLD-RE-DERIVE` (comparator): re-issue session GET and discard context before every task;
  memoryless-per-task. Predicted `0.875`; counters `(25, 0, 9, 1)`.
- `B-RETRIEVAL-SHAPED` (comparator): as cold plus one nearest-neighbour retrieval call per task over
  a store of PRIOR-session receipts; retrieves a stale foreign-session binding for the chain task.
  Predicted `0.875`; counters `(25, 8, 9, 1)`.
- `PC-EXACT-REPLAY` (positive control): given schema and binding by construction. Predicted `1.0`;
  counters `(17, 0, 8, 0)`.

Controls (stable ids):

- `NC-MECHANISM-OFF` (null/sensitivity): expose the binding via the session endpoint -> cold reaches
  `1.0` and the certificate becomes FALSE. A certificate that survives this is insensitive.
- `NC-EMPTIED-CONTEXT` (diagnostic): comparator with the frozen in-session binding removed -> tracks
  `0.875` at novelty >= 0.50.
- `NC-RETAIN-RECEIPT` (amortization-boundary diagnostic): retain only the immediate predecessor
  receipt -> `1.0` at novelty 0.50 (carry distance 1), `0.875` at novelty 0.75 (carry distance 2).
- `NC-NO-DISCOVERY-DIRECT`: valid session token but ignores schema/receipts -> `1.0` at novelty 0.00,
  `0.0` at novelty >= 0.25.
- `NC-BINDING-UNIQUENESS`: 160/160 scored bindings pairwise distinct (48-bit).
- `NC-NO-LEAK` (contamination gate F-LEAK; P2-WP003 guard): the binding appears in no session/task
  body, no error body and no log line; only in its own precursor receipt.
- `NC-MEMORYFUL` (DISCLOSED boundary diagnostic, NOT a certificate input): a within-session-memoryful
  cold agent reaches `1.0`. This is reported explicitly as the honest amortization boundary of this
  construction, so the certificate is never presented as an agent-capability claim.

## 6. Pre-freeze arithmetic certificate

Because exactly one of `K` tasks per session (the chain task) is satisfiable only via the one-time
binding, each memoryless-per-task comparator succeeds on exactly `K-1` tasks, i.e. rate
`(K-1)/K`. For `K = 8` that is `0.875`, inside the band `[0.80, 0.95)`. `K`-sweep `{7: 6/7,
9: 8/9, 10: 9/10}` = `{0.8571, 0.8889, 0.9}` all remain in band, and none collides with `0.95` or
`0.80`. Success margin `T - comparator = 0.125 >= 1/8`; matched-correctness floor `0.80`
(exact-match scoring, so `matched_correctness == success_rate`).

## 7. Decision rule (arithmetic, pre-freeze)

- A family certifies iff at novelty >= 0.50 COLD < 0.95 AND RETRIEVAL < 0.95 AND every scored arm
  has success_rate >= 0.80 AND matched_correctness >= 0.80 at every band AND behavioural
  distinction holds (>= 2/4 counter dimensions distinct T-vs-each-comparator AND margins >= 1/8).
- `SUPPORTS`: >= 1 family certifies AND V1-V7 pass AND NC-NO-LEAK clean AND liveness holds
  (PC = 1.0, T >= 0.80) AND diagnostics consistent with the non-degenerate reading -> deliver the
  certified bank as a reusable B2 substrate (substrate-validity evidence only; no promotion).
- `FALSIFIES`: zero families certify AND V1-V7 pass AND NC-NO-LEAK clean AND liveness holds AND
  non-certification is comparator-attributable (both families' comparators >= 0.95) -> bounded
  substrate-class negative; freeze nothing.
- `MIXED`: exactly one family certifies, or a diagnostic control is inconsistent (mechanism-off does
  not flip, retain-receipt anomalous), or liveness fails, or F-LEAK fires -> diagnosis required.
- `MEASUREMENT_INVALID`: any V1-V7 gate fails -> infrastructure/validity failure, not a scientific
  result.

All four branches are reachable; verified at DESIGN by a rule-level classifier over synthetic worlds
(probe `branch_reachability`, `all_branches_inhabited=true`).

## 8. Measurement validity gates

- V1 code fidelity manifest: sha256 of every EXECUTE-authored harness file + `python3 --version`
  recorded in `result.json.artifacts`; harness reconstructed only from frozen literals.
- V2 transport conformance: the full HTTP surface passes a conformance gate before scoring.
- V3 no leak: NC-NO-LEAK (F-LEAK) clean.
- V4 determinism: two identical runs byte-identical; deterministic `server_secret`.
- V5 arm liveness: T = 1.0 and PC = 1.0 at every band.
- V6 counter instrumentation: all four counters with matched accounting.
- V7 matched correctness: exact-match scoring; `matched_correctness == success_rate`.

## 9. Design-time satisfiability probe (non-outcome-bearing)

A cheap DESIGN probe (`design_satisfiability_probe` in `spec.json`, embedded in full with its
sha256) verified, without running the scored 20-session matrix: stdlib HTTP transport; 7/7 protocol
invariants; treatment liveness 8/8 at every band and PC 8/8; the predicted arm vectors
(T/PC = 1.0; COLD/RETRIEVAL = 0.875 with the predicted counters); the `K`-sweep arithmetic;
160/160 binding uniqueness; mechanism-off destroys the certificate; and all four decision branches
inhabited. `certificate_satisfiable=true`; two runs byte-identical. This confirms the design is
internally satisfiable before freeze; it is not a confirmatory measurement.

## 10. freeze_eligibility (design contract v2)

- `decision_rule_reachability`: PASS.
- `measurement_prerequisites`: PASS.
- `baseline_identifiability`: PASS.
- `control_sensitivity`: PASS.
- `treatment_liveness`: PASS.
- `freeze_artifacts_bound`: NOT_APPLICABLE -> `freeze_artifacts = []`. There is no pre-existing
  mutable local code/data/task-bank/fixture dependency; the substrate is generated from frozen
  literals and the EXECUTE harness is bound by the V1 code-fidelity manifest.

## 11. Threats to validity and scope

- Representation/ceiling risk: the certificate is intentionally defined against the B2 comparator
  conventions (B-COLD-RE-DERIVE memoryless-per-task; B-RETRIEVAL-SHAPED no cross-session mechanism).
  A within-session-memoryful agent reaches 1.0; this is disclosed as NC-MEMORYFUL and is a boundary
  of the certificate, not hidden.
- Single-construction risk: only one construction class and two families are tested; a FALSIFIES
  verdict is therefore explicitly bounded to this class, not to asymmetric discovery in general.
- Contamination risk: leakage of the binding would inflate comparator success; guarded by F-LEAK.
- This is DESIGN only: no outcome-bearing measurement is run here, and no preregistration term may
  be weakened after outcomes are seen.

## 12. Consequences

- Positive: a frozen, reusable B2 substrate with an arithmetically checkable pre-freeze dynamic-range
  certificate; the flagship four-arm inheritance benchmark becomes fundable with measurable range.
- Negative: a bounded substrate-class negative for credential-free asymmetric discovery, recorded
  first-class; no substrate is frozen and the director must choose a different level of description
  rather than re-discover the ceiling. Both outcomes remove the current critical-path ambiguity.
