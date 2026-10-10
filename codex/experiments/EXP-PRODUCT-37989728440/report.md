# Report: EXP-PRODUCT-37989728440 (product lane)

**Status:** COMPLETE · **Outcome:** FALSIFIES (bounded substrate-class negative) · **Frozen design:** `spec.json` / `prereg.md` (hashes in `freeze.json`).

This report explains and bounds the machine handoff in `result.json`. It does not exceed the frozen claim or contradict `result.json`.

## 1. What was executed

The frozen design was executed exactly: a credential-free, deterministic (SEED=42) localhost `http.server` substrate on which the correct action is **not** determined by the task specification and must be obtained by explicit discovery (`GET /api/session`, `GET /api/resources`, `GET /api/schema/{type}`), two task families (F1 documents/records, F2 widgets/gadgets), four novelty levels (0.0/0.25/0.5/0.75), 40 held-out tasks, 20 training tasks, and 30 known-negative cases. The treatment carrier is the audited kernel blob `b15ed848` (sha256 `718efa6a…`), vendored byte-identically at `harness/audited_spider/kernel.py` and `kernel_treatment.py`; the shipped `src/spider/kernel.py` was not touched.

Raw evidence is in `raw_evidence/`; derived measurements in `derived/`.

## 2. Central result: the dynamic-range certificate is false

The prereg's hard gate (C1) requires that, computed from the frozen task bank and frozen arm implementations **without run data**, `B-COLD-RE-DERIVE` or `B-RETRIEVAL-SHAPED` have `success_rate < 0.95` at novelty ≥ 0.5 in at least one family. It does not.

| Family | cold @0.5 | cold @0.75 | retrieval @0.5 | retrieval @0.75 |
|---|---|---|---|---|
| F1 | 1.000 | 1.000 | 1.000 | 1.000 |
| F2 | 1.000 | 1.000 | 1.000 | 1.000 |

Design-level certificate (computed before any arm ran): `false`. Observed certificate after the run: `false`. The two comparators both implement the mandatory discovery and the deterministic server accepts the discovered, in-support values, so every task is solvable. The task bank has **zero headroom** on this substrate class.

## 3. Why the certificate is unsatisfiable here

Discovery is a *shared* mandatory cost. For any arm to act, it must read the session token, the valid resource identifier, and (at novelty 0.75) the endpoint variant. No arm can act without those HTTP round-trips. The treatment does not replace them; it performs the same discovery and additionally pays one `retrieval_calls` unit for the registry lookup. A diagnostic confirms the premise that the action is genuinely unspecified: `D-DIRECT-NO-DISCOVERY` succeeds 10/10 at novelty 0.0 and 0/10 at novelty 0.5 and 0.75.

## 4. The C-RESIDUAL-NOVELTY economics test (C2–C5)

Per-arm pooled `cost_per_success` (frozen formula including `latency_ms/1000`):

| Novelty | T-SPIDER-PARAM | B-COLD-RE-DERIVE | B-RETRIEVAL-SHAPED |
|---|---|---|---|
| 0.0 | 4.00 | 2.00 | 6.00 |
| 0.25 | 4.00 | 4.00 | 6.00 |
| 0.5 | 5.00 | 5.00 | 7.00 |
| 0.75 | 6.00 | 6.00 | 8.00 |

- **C2 (matched correctness): PASS.** All four main arms reach `success_rate = 1.0` at every level.
- **C4 (treatment cheaper than retrieval): PASS, but trivially.** The treatment is 2 units cheaper at every level, entirely because `retrieval_calls` is 1 versus 3. No `http_requests` are saved.
- **C3 (treatment cheaper than cold): PASS only as measurement noise.** On deterministic counters the treatment *ties* cold at 0.25/0.5/0.75 (4/4, 5/5, 6/6) and is *worse* at 0.0 (4 vs 2). The frozen metric includes `latency_ms/1000`; the tiny numeric "wins" at 0.25/0.5/0.75 (~1e-4…9e-4 on a 2–6 unit base) are instrument noise. `result.json.metrics.c3_c4_robustness` records `C3_counter_only = false`.
- **C5 (advantage increases with residual novelty): FAIL.** Vs cold, Spearman ρ = 0.586 but permutation p = 0.153 (not significant), and the task-length confound control is ρ = 0.586 > 0.3 — the apparent trend is exactly the task-length trend. Vs retrieval the (latency-inclusive) advantage is flat near +2.0 at every novelty level (ρ = 0.000, p = 1.0; counter-only ρ = 0.0, p = 1.0): the treatment's saving over retrieval does **not** scale with novelty at all. Values as recorded in `derived/spearman_monotonicity.json` (SEED=42, 10,000 permutations).

The hypothesis's proposed mechanism — parameterized discovery sub-mechanisms reduce `http_requests` — does not materialize, because discovery is mandatory and symmetric across arms. This is a measured result, not an assumption.

## 5. Controls and attribution

- `B-EMPTIED-REGISTRY` matched cold to within 7.6e-5 relative difference at every point (C6 PASS): the registry, not an artifact of the harness, is the carrier of any treatment behavior.
- `B-LITERAL-KERNEL` returned EXPLORE on all 200 held-out tasks (success 0.0), isolating the parameterized path (C9 PASS).
- `PC-EXACT-REPLAY` executed 20/20 training tasks through the distilled mechanism (C9 PASS).
- Known negatives: 30/30 refused, `bound_action = null`, correctly categorized reasons (C7 PASS).
- `model_calls = 0`, `model_tokens = 0`; `retrieval_calls` as designed (treatment 1, cold 0, retrieval 3, empty 0) (C8 PASS).
- Real localhost HTTP, two families, four-level gradient, distinct from the prior one-request synthetic fixtures (C10 PASS).
- Treatment carrier hash-verified against `b15ed848` (C11 PASS).

## 6. The freeze-gate defect (governance finding)

`spec.json` and `prereg.md` §7.1/§11 assert that the pre-freeze certificate is enforced "by the freeze script reading `spec.json.dynamic_range_certified`". This is **not true**:

- `scripts/freeze_experiment.py` required-key list (lines 42–47) omits `dynamic_range_certified` and contains no certificate computation;
- no reference to `dynamic_range` exists anywhere under `scripts/` or `.github/`;
- `spec.json` contains no `dynamic_range_certified` field.

Consequently `freeze.json` exists for a packet whose C1 certificate is false. This packet was already frozen, so EXECUTE proceeded and recomputed the certificate. The defect should be repaired before further packets rely on the gate.

## 7. Interpretation (bounded)

The evidence falsifies, **for this mandatory-discovery deterministic REST substrate class**, the proposition that a certified dynamic range can be produced for these four arms: both comparators sit at the 1.0 correctness ceiling, so no economics comparison can discriminate the kernel's parameterized path from cold re-derivation. It does **not** show that no credential-free substrate can have dynamic range, nor that parameterized inheritance lacks value on other substrates. The treatment never demonstrably compresses work here.

The appropriate next step (per the Director mandate's negative branch) is not to re-run this certificate or to promote kernel parameterization, but to route the shared task-bank problem to the external-agent four-arm benchmark on a provisioned model endpoint, where genuine behavioral variance can create dynamic range.

## 8. Classification note

The frozen OVERALL rule is internally ambiguous: it lists both `FALSIFIES` ("C1 fails (certificate unsatisfiable)") and `MEASUREMENT_INVALID` ("C1 fails at freeze time"). This run's measurements are valid, deterministic and reproducible, so `status = COMPLETE` with `outcome = FALSIFIES` was chosen, consistent with the packet contract that a valid negative is normally COMPLETE. The parent experiment encoded the analogous situation as `MEASUREMENT_INVALID`; the DIRECTOR may prefer that convention. All raw facts are preserved for reclassification without re-running.
