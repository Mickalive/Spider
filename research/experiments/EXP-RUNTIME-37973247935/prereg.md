# Preregistration: EXP-RUNTIME-37973247935

## Lane: runtime
## Claim: C-MEAS-VALID (Measurement substrate is intervention-valid)
## Experiment ID: EXP-RUNTIME-37973247935
## Parent: EXP-RUNTIME-36293257855 (frozen, VALIDATED at the authorship-separated real-Chromium scope)
## Director mandate: action=CONTINUE, claim=C-MEAS-VALID (request.json `director_mandate`)

---

## 0. Inheritance (from the exact parent handoff)

This section preserves the four-way distinction of `research/experiments/EXP-RUNTIME-36293257855/handoff.json` (sha256 `edd619165519091a4127188b2c1eaa652217963d1d99223afee312ca2ef93b5f`). It is inherited state, not an agenda. The binding direction is the Director mandate in `request.json`.

### established (do not re-measure; may be cited at exactly this ceiling)
- C-MEAS-VALID is VALIDATED at the parent audit claim_ceiling: the composite oracle (length-framed SHA-256 over `/tmp/single.db` plus `/tmp/single.db-wal` + SQL logical projection of the controlled row + stable-header response fingerprint) maintains arm-constrained discrimination across the author/measurer and transport boundaries simultaneously. Parent numbers: P-WRITE/P-DRIFT sensitivity 20/20 point 1.0 Wilson95 [0.8388748419471806, 1.0]; N-READ/N-INVALID/N-EXPIRED/N-DELETED specificity 20/20 point 1.0 same interval; positive control 1.0; all four nulls 1.0 with zero false positives; independent recomputation zero_mismatches; all required capability-ledger scopes PASS; AUDIT PASS, no required fixes.
- Authorship separation exists as durable separable components: `intervention_surface.py` (ground-truth provider; no scorer import) and `oracle_scorer.py` (detector; no Flask, no surface import), sharing only constants-only `shared_config.py`.
- Real-browser transport with writes is proven: 120/120 episodes via the public Playwright API, real `page.click` as the only write mechanism, CDP DOM + AX captured per episode, no synthetic fallback.
- The one-command fail-closed capability contract (`bringup.py` + per-experiment `bringup_contract.json`) executes and passes; readiness floors met (240/240 non-304, 2 workers, stickiness 1.0 over 12 URIs, cache MISS-then-HIT).
- Durability is a two-part fact: DURABILITY_status UNSATISFIABLE / REFERENCE_ONLY at measurement (scientific_effect none), and the six frozen-scope paths are HEAD-resident and byte-equal at decision-time HEAD `38c23efa`.

### rejected (do not revive as explanations)
- "The oracle only discriminates because the same author wrote the surface and the detector" — separate modules, no cross-imports, scorer receives no arm label/planted value/token class.
- "Browser writes cannot run here" — 120/120 episodes and a restore control ran through the canonical Chromium.
- "Audit PASS licenses PRODUCT_CORE/SHIPPED" — no Product-lane frozen gate; `promote_to_product=false`.
- "Perfect 1.0 point rates imply production readiness or a bound tighter than Wilson_lo 0.8388748419471806 at n=20."
- "The durability UNSATISFIABLE record is a falsification" — it is a contract result with scientific_effect none.
- "A future control is discriminating merely because it reports pass" — this program's recurring defect is controls/branches that cannot fire.

### unknown (carried explicitly into this design)
- Whether the oracle's discrimination transfers to a change it did not author: an out-of-surface worker, cache or representation transition → **the primary question of this experiment**.
- Whether a write-then-revert inside the capture interval is visible to the byte-equality WAL oracle at all → **measured by this experiment's blind-spot probe**.
- Whether any downstream lane ever preregisters this substrate as a precondition (publication is not adoption).
- Whether the ceiling should widen to production auth, TLS, HTTP/2, multi-host, real sites.
- Whether the 1.0 rates persist at larger n or on a second run.

### do_not_assume (dangerous non-conclusions preserved)
- Do not read C-MEAS-VALID=VALIDATED as validating production systems, TLS, HTTP/2, real websites or any downstream lane's own surface.
- Do not treat P-WRITE/P-DRIFT as evidence about real-world drift — both are planted through the surface's own endpoints.
- Do not assume the byte-equality oracle detects a write reverted inside the interval; do not assume the 10/10 stability control rules that out. It bounds spontaneous variation only.
- Do not schedule a durability re-experiment (paths are HEAD-resident).
- Do not infer product promotion from any status here.
- Do not re-run the plain-HTTP or browser six-arm matrix at the same scope **as a scientific question**. This experiment re-runs only a small in-surface control (`PC-INSURFACE-WRITE-LIVE`) for instrument liveness, explicitly labeled as a control.
- Do not accept a control as discriminating merely because it reports pass.
- Do not treat browsergym/agentlab/policy-model credentials/GHCR as available; the design below is credential-free and declares them advisory.

### Director mandate disposition
`parent_handoff_disposition = USE`. The mandate's strategic question is reproduced in Section 1 and converted into a falsifiable test without drifting to a nearby continuation. Agent priors recorded in `request.json.director_mandate.agent_priors_used` are treated as priors, not SPIDER evidence.

---

## 1. Strategic Question (binding, from the Director mandate)

With the composite intervention oracle VALIDATED only at the authorship-separated, real-Chromium-transport scope and only against interventions the fixture's own controlled endpoint planted:

> Does the same oracle retain arm-constrained discrimination — point sensitivity/specificity ≥ 0.90 with two-sided 95% Wilson lower bound ≥ 0.80, non-degenerate intervals, zero false positives on matched nulls, arm-blind scoring and independent recomputation with zero mismatches — when the change it must detect is induced **OUTSIDE** the surface the detector's author wrote (a component that is not `research/runtime/intervention_surface.py` and not reachable from the scorer), while a powered write-then-revert probe executed entirely inside the 50 ms capture interval is added to **MEASURE** (not assume away) the acknowledged blind spot of a byte-equality WAL oracle?

The experiment also records whether a positive result licenses treating the substrate as measurement-valid for downstream real-drift questions and a local delta-repair substrate (Section 15). Licensing is a DIRECTOR decision; this packet only narrows the construct boundary.

---

## 2. Hypothesis

The oracle's arm-constrained discrimination is a property of the oracle over **committed database state transitions**, not an artifact of the fixture that authored the interventions.

- **H1 (out-of-surface sensitivity).** Out-of-surface committed mutations are detected at point sensitivity ≥ 0.90 with Wilson 95% lower bound ≥ 0.80 and non-degenerate intervals, for both:
  - `P-OOS-WORKER` (direct SQLite UPDATE of the controlled `runtime_probe` row), and
  - `P-OOS-REPR` (direct SQLite UPDATE of `body_config` changing the body served by the stable-header `/api` endpoints).
- **H2 (out-of-surface specificity).** Matched out-of-surface nulls produce zero false positives:
  - `N-OOS-IDLE` (worker invoked, read-only, no commit),
  - `N-OOS-REJECT` (worker mutation violates `CHECK(id=1)`, rolled back before commit),
  - `N-OOS-CACHE` (nginx cache MISS→HIT over an identical body/stable headers).
- **H3 (instrument liveness).** The unchanged in-surface planted browser write (`PC-INSURFACE-WRITE-LIVE`) is still detected at sensitivity 1.0 in this run.
- **H4 (blind-spot, measured not gated).** A write restored to byte-identical pre/post state inside the interval is not detected (`M-REVERT-BYTES` → detect ≈ 0), while a logically-reverted but not byte-restored write is detected (`M-REVERT-LOGICAL` → detect ≈ 1).

---

## 3. Falsifier

Any of the following is an explicit falsification of the transfer hypothesis:

1. Either `P-OOS-WORKER` or `P-OOS-REPR` yields point sensitivity < 0.90, **OR** Wilson 95% lower bound < 0.80, **OR** a degenerate interval (ci_hi ≤ ci_lo) — given that the liveness control passed.
2. Any single false positive (`detected=true`) on any matched out-of-surface null episode in `N-OOS-IDLE`, `N-OOS-REJECT`, `N-OOS-CACHE` (zero false positives is the frozen null requirement).
3. Independent recomputation over raw JSONL yields `zero_mismatches=false`.
4. The arm-blind discipline is violated (detector output written after arm labels are joined).

Instrument-liveness failure, capability-ledger required-scope failure, missing mandatory WAL evidence, authorship/reachability violation, synthetic fallback, or a failed pre-freeze preflight are **not** scientific falsification and map to `INCONCLUSIVE` or `MEASUREMENT_INVALID` (Section 11). The blind-spot probe never falsifies the transfer hypothesis.

---

## 4. Baseline (frozen reference, not re-measured)

`B-INSURFACE-BROWSER-VALIDATED` from EXP-RUNTIME-36293257855: composite oracle; 6 in-surface arms × 20 episodes through real Chromium; all arms point=1.0, Wilson95=[0.8388748419471806, 1.0]; positive control 1.0; null-matrix specificity 1.0; zero false positives; arm-blind; recompute zero_mismatches; capability ledger required scopes PASS; AUDIT PASS.

`B-OUT-OF-SURFACE-PRECEDENT`: none. The Codex and the parent handoff record that an out-of-surface transition has never been measured; the cache MISS→HIT exists only as a readiness diagnostic and `P-DRIFT` is a surface-planted `set_representation`. Recorded as `{}` rather than fabricated.

The baseline's constructive bound — **all positive changes were performed through the surface's own endpoint** — is precisely what this experiment tests.

---

## 5. Experimental Design

### 5.1 New out-of-surface arms (5 arms × 40 episodes = 200 episodes)

| Arm | Type | Inducing component | Action inside the measured interval | Expected committed change | n |
|-----|------|--------------------|--------------------------------------|---------------------------|----|
| `P-OOS-WORKER` | Positive | `oos_worker.commit_probe_update` (direct SQLite, not the surface) | `UPDATE runtime_probe SET marker=?, revision=revision+1, updated_at=? WHERE id=1; COMMIT` | WAL bytes change; logical projection changes | 40 |
| `P-OOS-REPR` | Positive | `oos_worker.commit_representation` (direct SQLite, not the surface) | `UPDATE body_config SET variant=?, content=? WHERE id=1; COMMIT` | WAL bytes change; served body → fingerprint changes | 40 |
| `N-OOS-IDLE` | Null | `oos_worker.idle` | connect, read-only SELECT, close | none | 40 |
| `N-OOS-REJECT` | Null | `oos_worker.reject_rollback` | attempt `CHECK(id=1)` violation, then ROLLBACK | none committed | 40 |
| `N-OOS-CACHE` | Null | exclusive nginx `proxy_cache` | two requests on one fresh cacheable key → MISS then HIT, identical body | none | 40 |

**Matching argument.** `N-OOS-IDLE` is the matched null of both positives on the worker path (same component, same connection path, no commit). `N-OOS-REJECT` is the matched transactional null (same component attempts a real write but no bytes commit). `N-OOS-CACHE` is the matched null for a representation transition performed by a non-surface component (the proxy) where the semantic content and stable headers are identical, so only the frozen-volatile excluded headers (`X-Cache`, `Age`, `X-Worker-Pid`) differ.

**Why n=40.** See the attainability certificate (Section 10): at n=20 the frozen pair (point ≥ 0.90 AND Wilson_lo ≥ 0.80) is satisfiable only at 20/20; a single miss on a genuinely 0.95 instrument would FALSIFY. At n=40 the accept region is non-empty and non-trivial (k ≥ 37, point ≥ 0.925, Wilson_lo ≥ 0.8014), so the literal Director thresholds are attainable by a genuinely high-rate instrument, not only by a perfect one.

### 5.2 Instrument-liveness control (in-surface, 20 episodes)

`PC-INSURFACE-WRITE-LIVE`: a planted valid-auth SPA write through a REAL Chromium button click against the UNCHANGED validated `intervention_surface.py`, exactly as the parent P-WRITE arm. Expected: detected 20/20; pre/post WAL vector differs; logical projection matches the planted value. This re-establishes instrument liveness and separability in this run. It is a control, not the scientific question; it does not repeat the six-arm matrix.

### 5.3 Blind-spot probe (measured, not gated; 2 sub-conditions × 20 episodes)

`M-REVERT-BLINDSPOT`, executed entirely inside the 50 ms capture interval:
- `M-REVERT-BYTES`: snapshot the exact bytes of `/tmp/single.db` and `/tmp/single.db-wal`; commit an out-of-surface mutation; independently confirm the write happened via direct SQL; restore the snapshot bytes exactly. Registered directional prediction: oracle detects ≈ 0.
- `M-REVERT-LOGICAL`: commit an out-of-surface mutation; then commit the compensating inverse (logical state restored, WAL retained). Registered directional prediction: oracle detects ≈ 1.

Each probe episode records `write_happened` (independent SQL confirmation), `revert_bytes_identical` (pre-vector == post-vector), and `detected`. Report the detection fraction per sub-condition with a Wilson CI. The probe never gates `SUPPORTS`/`FALSIFIES`; it updates interpretation, `validity_notes` and `unresolved`.

---

## 6. Components and Authorship Separation (Mandatory)

### 6.1 Out-of-surface worker — `research/runtime/oos_worker.py` (NEW)
- Ground-truth provider for the out-of-surface arms (the analogue of `intervention_surface.py` for this new scope).
- Modes: `commit_probe_update`, `commit_representation`, `idle`, `reject_rollback` (Section 5.1).
- Connects directly to `/tmp/single.db` with `wal_autocheckpoint=0`; bypasses the Flask surface entirely.
- **Must NOT import**: `intervention_surface.py`, `oracle_scorer.py`.
- **Must NOT be imported by**: `oracle_scorer.py`.
- Records its own raw evidence per invocation (mode, SQL, before/after row, committed, exception).

### 6.2 Detector — `research/runtime/oracle_scorer.py` (UNCHANGED)
- Reused byte-for-byte from the validated parent (`wal_vector_capture`, `logical_projection`, `response_fingerprint`, `detect`, `wilson_ci`). Its hash must remain `7a30ff637654fbfc366d0f0b1dbe2f8bc481c9b56f5ee48fd894e12baccdad5f`.
- Imports no Flask, no surface, no out-of-surface worker.
- `detect()` receives only the three raw measurements and never an arm label, planted value, worker mode or expected outcome.

### 6.3 Intervention surface — `research/runtime/intervention_surface.py` (UNCHANGED)
- Reused from the validated parent for the in-surface liveness control and fixture plumbing only. Its hash must remain `10be3dcb8bed76c8d215916aa9b5b2fb8cf95ede8a6136eedd5b948ba1ea0705`.

### 6.4 Shared constants — `research/runtime/shared_config.py` (UNCHANGED)
- Constants only. The new arm matrix, n, seeds and thresholds for this experiment live in an experiment-local config under `research/experiments/EXP-RUNTIME-37973247935/` so the validated component hashes are not mutated.

### 6.5 Harness — `research/experiments/EXP-RUNTIME-37973247935/run_experiment.py` (NEW)
- Imports both the surface and the out-of-surface worker, plus the unchanged scorer; contains **no** intervention logic and **no** detection logic.
- Orchestrates: bring-up → fixture setup (outside interval) → episode loop → capture → arm-blind scoring → label join → metrics.
- Scorer unreachability of `oos_worker.py` is enforced by a static source scan (`V-OOS-UNREACHABLE-FROM-SCORER`).

**Honest representation loss.** Multi-human authorship is not observable in this environment. What is measured is **logical component separation and scorer-unreachability** at the module boundary prescribed by the mandate; this is recorded in `validity_notes` and `unresolved`.

---

## 7. Transport (unchanged from the validated parent)

- Playwright 1.63.0 public API only; `p.chromium.executable_path` launch of `/home/runner/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome`, sha256 `8c599d43aec53f2460a31ae2f4af6bd863f8258b34ff519564bc5d4726bfaa1e`, version 153.0.8010.12; viewport 1280×720.
- Per episode inside the measured interval: navigate (as per arm), 50 ms quiescence, capture before (WAL vector, logical projection, response fingerprint, CDP DOM `DOM.getDocument(depth=-1, pierce=True)`, `Accessibility.getFullAXTree`), execute the arm action, wait for network idle + 50 ms quiescence, capture after.
- Real button clicks remain the ONLY write mechanism for the in-surface liveness control and for navigation. The new out-of-surface mutation is performed by `oos_worker.py` executed by the harness and is deliberately NOT routed through any browser click or through `intervention_surface.py`.
- Fixture setup/teardown (session upsert, probe reset, body reset) happens OUTSIDE the measured interval and is recorded per episode.
- No `httpx`/`requests` fallback; no synthetic browser, WAL, DOM, AX or credential substitution.

---

## 8. WAL Byte Evidence (Mandatory)

- Vector = length-framed SHA-256 over the concatenation of `/tmp/single.db` and `/tmp/single.db-wal`, both fully read and length-prefixed; `-shm` recorded diagnostically only.
- Captured inside the measured interval after 50 ms quiescence.
- Artifact `artifacts/A-WAL-VECTOR-BEFORE-AFTER.jsonl`: one record per episode with `episode_id`, `before_hash`, `after_hash`, `wal_changed`.
- Stability control (`NC-CAPTURE-STABILITY`): 20 no-action pairs, all must be byte-identical, bounding spontaneous variation. This does NOT rule out a transient write-then-revert; that case is measured by `M-REVERT-BLINDSPOT`.

---

## 9. Arm-Blind Scoring and Independent Recomputation

1. Pre-seeded RNG generates the episode order; archived before any episode runs (`artifacts/A-SEEDED-ORDER.json`).
2. The detector runs on all episodes WITHOUT arm labels and writes `artifacts/A-DETECTOR-OUTPUT.jsonl` (`episode_id`, `detected`, `wal_changed`, `logical_changed`, `fingerprint_changed`).
3. Arm labels are joined only after the detector output exists; per-arm sensitivity/specificity with two-sided 95% Wilson intervals.
4. Independent recomputation `artifacts/A-RECOMPUTE-CHECK.json` re-implements the detector and Wilson CI from raw JSONL only, imports nothing from `oracle_scorer`, and must yield `zero_mismatches=true`.

---

## 10. Pre-freeze Attainability and Control-Liveness Certificate (mandatory)

### 10.1 Arithmetic attainability (computed in DESIGN, pure arithmetic, no outcomes)

Frozen z = 1.959963984540054; two-sided 95% Wilson score interval.

| Arm class | n | accept region | point at boundary | Wilson_lo at boundary | non-degenerate |
|-----------|---|---------------|-------------------|-----------------------|----------------|
| out-of-surface positive | 40 | k ≥ 37 | 0.925 | 0.8014 | yes |
| out-of-surface null (zero FP) | 40 | k = 40 (0 FP) | 1.0 | 0.9124 | yes |
| in-surface liveness control | 20 | k = 20 | 1.0 | 0.8388748419471806 | yes |

Reference values establishing that n=20 would be brittle for positives: k=19/20 → Wilson_lo 0.7639 (< 0.80, fails); k=18/20 → 0.6990. At n=40, k=37/40 → 0.8014 (passes). This certificate must be reproduced as `artifacts/A-ATTAINABILITY-CERTIFICATE.json` (full k=0..n table) before freeze.

### 10.2 Structural control-liveness checks (must all pass before freeze)

Run mechanically on a throwaway DB copy / throwaway cache key; **never** invoke `oracle_scorer` on real episodes and **never** inspect arm outcomes:

| id | check |
|----|-------|
| `CL-OOS-WORKER-COMMIT-PROBE` | `commit_probe_update` produces a committed WAL byte change and changed logical row on a throwaway copy |
| `CL-OOS-WORKER-COMMIT-REPR` | `commit_representation` changes `body_config` and therefore the served body on a throwaway copy |
| `CL-OOS-WORKER-IDLE` | `idle` leaves throwaway DB+WAL bytes byte-identical |
| `CL-OOS-WORKER-REJECT` | `reject_rollback` raises the CHECK constraint, rolls back, leaves bytes byte-identical |
| `CL-REVERT-FIDELITY` | snapshot/restore of DB+WAL bytes yields a byte-identical vector on a throwaway copy |
| `CL-CACHE-MISS-HIT` | a fresh cacheable key yields MISS then HIT with identical body and identical stable headers |
| `CL-INSURFACE-LIVE` | the unchanged surface still mutates the WAL via a real browser click (parent-proven; structurally re-verified) |

**Failure discipline.** A failed arithmetic or liveness check blocks freeze and makes the experiment `MEASUREMENT_INVALID`, never a scientific negative. This responds directly to the program's recurring defect: frozen branches and controls that cannot fire.

---

## 11. Decision Rule (Frozen)

| Outcome | Condition |
|---------|-----------|
| **SUPPORTS** | Both `P-OOS-WORKER` and `P-OOS-REPR`: point ≥ 0.90 ∧ Wilson_lo ≥ 0.80 ∧ ci_hi > ci_lo. Zero false positives across all 120 matched out-of-surface null episodes. `PC-INSURFACE-WRITE-LIVE` sensitivity = 1.0. Arm-blind output archived before label join. Recomputation `zero_mismatches=true`. Capability ledger all required scopes PASS. Attainability + control-liveness preflights passed. |
| **MIXED** | Exactly one out-of-surface positive passes and the other fails; OR both positives pass but ≥ 1 matched-null false positive (sensitivity transfers, specificity does not); OR both positives pass but the blind-spot probe contradicts both registered directional predictions (interpretation only; never changes the gate). |
| **FALSIFIES** | Both out-of-surface positives fail the positive thresholds while the liveness control passed; OR zero false positives is violated together with at least one positive failing. `status=COMPLETE` with this outcome. |
| **INCONCLUSIVE** | Infrastructure/substrate failure prevents completing the frozen matrix; OR capability-ledger required scope FAIL; OR mandatory WAL evidence missing; OR the number of scored episodes per arm differs from n for mechanical reasons. Recorded per-episode with the smallest unblocking action. |
| **MEASUREMENT_INVALID** | Authorship separation or scorer-unreachability violated; synthetic fallback used; `PC-INSURFACE-WRITE-LIVE` sensitivity < 1.0 (instrument not live); attainability/control-liveness preflight not run or failed; WAL evidence captured outside the measured interval; probe snapshot/restore fidelity not achieved where required. |

The blind-spot probe `M-REVERT-BLINDSPOT` is reported with Wilson CIs and does not gate the mapping above.

---

## 12. Validity Threats and Mitigations

| Threat | Mitigation |
|--------|------------|
| Out-of-surface worker accidentally reaching the detector (shared import) | Static source scan `V-OOS-UNREACHABLE-FROM-SCORER`; `oracle_scorer.py` unchanged and hash-pinned; scorer receives only raw measurements. |
| A control passes because it cannot fire (program's recurring defect) | Section 10 control-liveness preflight is mandatory before freeze; every accept region is materialized arithmetically. |
| Spontaneous WAL variation inflating null false positives | `wal_autocheckpoint=0` on every connection; no other writers; 20 no-action stability pairs; fixture setup/teardown outside the interval. |
| `N-OOS-CACHE` silently hitting origin or bypassing cache | Cache leg is verified live (`X-Cache` MISS then HIT) inside the episode and by `CL-CACHE-MISS-HIT`; Authorization-bearing requests are cache-bypassed by design, so a cacheable unauthenticated stable key is used. |
| Out-of-surface write also mutating the surface's expected-projection bookkeeping (making the test not truly blind) | The mutation is applied by direct SQLite `oos_worker` bypassing `intervention_surface.py`; the surface is never told and its routes are not called for the new arms. |
| Byte-equality blind spot understated | `M-REVERT-BLINDSPOT` measures both byte-restore and logical-restore directions with independent write confirmation. |
| Multi-human authorship unobservable | Recorded honestly: measured object is logical component separation + scorer-unreachability (Sections 6 and 12; `unresolved`). |
| Probe snapshot/restore under live SQLite connections corrupts the substrate | Probe runs after quiescence; fidelity is asserted per episode and mechanically checked pre-freeze on a throwaway copy; non-fidelity is a fixture failure, not a detection. |
| 1.0 point rates over-read as certainty | Reported at the Wilson bound; the honest per-arm bound is the interval, not 1.0. |
| Deterministic seed leakage | Fresh per-case RNG with recorded seeds; order pre-archived. |

---

## 13. Artifacts to Produce

| Path | Role | Description |
|------|------|-------------|
| `artifacts/A-SEEDED-ORDER.json` | fixture | pre-archived episode order and per-episode seeds |
| `artifacts/A-DETECTOR-OUTPUT.jsonl` | raw | arm-blind detector output (no arm field) |
| `artifacts/A-WAL-VECTOR-BEFORE-AFTER.jsonl` | raw | pre/post WAL vector hashes per episode |
| `artifacts/A-EPISODE-LEDGER.jsonl` | raw | arm, mode, status, fixture timing, quiescence, logical marker/representation |
| `artifacts/A-CAPTURE-STABILITY.jsonl` | raw | 20 no-action byte-identical pairs |
| `artifacts/A-OOS-WORKER-EVIDENCE.jsonl` | raw | per-invocation mode/SQL/before-after/committed/exception |
| `artifacts/A-BLINDSPOT-PROBE.jsonl` | raw | per-probe `write_happened`, `revert_bytes_identical`, `detected`, sub-condition |
| `artifacts/A-DERIVED-METRICS.json` | derived | per-arm sensitivity/specificity + Wilson CIs; probe rates |
| `artifacts/A-RECOMPUTE-CHECK.json` | derived | independent recomputation `zero_mismatches` |
| `artifacts/A-AUTHORSHIP-CHECK.json` | raw | no cross-imports; scorer no Flask/surface/oos_worker |
| `artifacts/A-OOS-UNREACHABLE.json` | raw | static scan of scorer↔oos_worker import reachability |
| `artifacts/A-SYNTHETIC-CHECK.json` | raw | no forbidden HTTP clients / synthetic fallbacks |
| `artifacts/A-ATTAINABILITY-CERTIFICATE.json` | derived | full k=0..n Wilson table and accept regions |
| `artifacts/A-CONTROL-LIVENESS.json` | derived | pre-freeze control-liveness certificate (Section 10.2) |
| `artifacts/A-READINESS-CERTIFICATE.json` | raw | readiness floors + cache MISS-then-HIT |
| `artifacts/B-PLAYWRIGHT-CAPABILITY.json` | raw | browser launch receipt (path, sha256, version, viewport, CDP/AX) |
| `artifacts/B-WAL-EVIDENCE.jsonl` | raw | representative before/after WAL evidence per arm class |
| `artifacts/capability_ledger.json` | derived | fail-closed capability ledger |
| `artifacts/C-BRINGUP-CONTRACT.json` | derived | bring-up contract execution record |

`result.json`, `report.md` and `provenance.json` are produced by EXECUTE with the exact required top-level shapes.

---

## 14. Capability Ledger and One-Command Bring-Up

- `research/runtime/bringup.py` + per-experiment `bringup_contract.json`; exit 0 + `OK: all declared required scopes pass` required before any episode runs.
- Required scopes (fail-closed): `CAP-CHROMIUM-LAUNCH`, `CAP-WAL-SUBSTRATE`, `CAP-NGINX-PROXY`, reusing the validated parent contract and readiness floors (`n_non304 ≥ 200`, per endpoint ≥ 100, 2 distinct workers, stickiness ≥ 0.90 over > 10 URIs, 0 missing worker headers).
- Advisory UNAVAILABLE and explicitly NOT on the critical path: BrowserGym, AgentLab, policy-model credentials (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `HF_TOKEN`, `GITHUB_TOKEN`), GHCR. The out-of-surface design is credential-free and requires no model endpoint; a missing model credential cannot block this decision.

---

## 15. Product Consequences and Licensing

### 15.1 If SUPPORTS
- C-MEAS-VALID's construct boundary is materially narrowed: the instrument is shown to detect committed state transitions it did not author, not merely fixture-performed interventions.
- Downstream Graph (`C-FRESHNESS`, `C-DELTA-REPAIR`) and the Physics statistical-contract certification may preregister the substrate as a measurement-valid precondition **at the new, explicitly quoted ceiling**.
- `oos_worker.py` becomes a reusable component-level analogue of the intervention surface for future transfer tests.
- Still a bounded scope widening, not product promotion: runtime may not set `PRODUCT_CORE`/`SHIPPED`; that requires a Product-lane frozen gate and an independent PASS audit.

### 15.2 If MIXED / FALSIFIES
- The ceiling narrows to "the oracle detects what this particular fixture does"; downstream lanes may not inherit the substrate for real drift or delta-repair.
- The program must either (a) redesign the detector to key on a state-transition observable not tied to the authored fixture (e.g. an explicit logical-delta or versioned-projection channel) before downstream preregistration, or (b) publish the instrument as a fixture-scoped control and route freshness/repair to a different substrate.
- A MIXED result localizes the break to a component or channel and guides targeted repair instead of blanket rejection.

### 15.3 If INCONCLUSIVE / MEASUREMENT_INVALID
Infrastructure or validity failure — **not** a scientific result. Exact failure recorded with smallest unblocking action; no weakening of the preregistration after seeing outcomes.

---

## 16. Dependencies and Preconditions

1. The Director mandate in `request.json` (`action=CONTINUE`, `claim_id=C-MEAS-VALID`) is the binding direction.
2. The frozen parent packet `research/experiments/EXP-RUNTIME-36293257855/` is immutable and is cited, not re-measured.
3. Validated components at their recorded hashes: `oracle_scorer.py` `7a30ff637654fbfc366d0f0b1dbe2f8bc481c9b56f5ee48fd894e12baccdad5f`, `intervention_surface.py` `10be3dcb8bed76c8d215916aa9b5b2fb8cf95ede8a6136eedd5b948ba1ea0705`, `shared_config.py` `6840f540bb54ac2b9c047ff7a4a0170c5617b45b2066b0d8d7dbb6f1ee4d2215`, `bringup.py` `d6cc744b72b049e4b6706ccdfb31b97276dbf8d413fe770886a468f956a68103`.
4. Live substrate contract: 2× gunicorn 23.0.0 on 127.0.0.1:19860/19861 sharing `/tmp/single.db` with `wal_autocheckpoint=0`, exclusive nginx 1.24.0 on 127.0.0.1:19851 with one `hash $request_uri consistent` upstream and real `proxy_cache`, plus the frozen readiness floors.
5. Canonical Chromium to be re-verified at run time, not assumed: sha256 `8c599d43aec53f2460a31ae2f4af6bd863f8258b34ff519564bc5d4726bfaa1e`, Playwright 1.63.0 public API only.
6. `research/runtime/oos_worker.py` and the experiment-local harness must exist, be HEAD-resident, and pass their control-liveness checks before freeze.
7. Physics owns certification of the statistical contract; runtime must not duplicate it.
8. Downstream consumers: Graph C-FRESHNESS / C-DELTA-REPAIR and the Physics statistical-contract certification.

---

## 17. Non-Goals (Explicitly Out of Scope)

- Production OAuth/OIDC, TLS, CDN, load balancer, HTTP/2, multi-host, real sites.
- BrowserGym, AgentLab, policy-model integration, LLM inheritance, cross-site transfer.
- Re-running the six-arm in-surface matrix as a scientific question (only the labeled liveness control is re-run).
- A durability re-experiment (paths are HEAD-resident).
- Any product promotion or claim-registry edit by this packet; the DIRECTOR owns verdicts.
- Generalizing the out-of-surface result beyond the declared component set and localhost fixture.

---

## 18. Seed and Determinism

- Master seed derived from `experiment_id` 37973247935.
- Episode order: `random.Random(master_seed).shuffle(...)`, archived before episode 1 in `artifacts/A-SEEDED-ORDER.json`.
- Per-episode RNG: `random.Random(master_seed + episode_index)`.
- All seeds recorded in `A-SEEDED-ORDER.json` and `provenance.json`. No code path branches on arm id inside the detector.

---

## 19. Freeze Checklist (before `freeze.json`)

- [ ] `research/runtime/oos_worker.py` exists with modes `commit_probe_update`, `commit_representation`, `idle`, `reject_rollback`; imports neither the surface nor the scorer.
- [ ] `oracle_scorer.py`, `intervention_surface.py`, `shared_config.py` byte-hashes equal the validated parent hashes (unchanged).
- [ ] `run_experiment.py` imports the surface, the out-of-surface worker and the scorer but contains no intervention or detection logic.
- [ ] `A-ATTAINABILITY-CERTIFICATE.json` reproduced (accept regions: positive k ≥ 37/40; null 0 FP; liveness 20/20).
- [ ] All `CL-*` control-liveness checks pass on throwaway copies, without invoking the detector on real episodes.
- [ ] `A-OOS-UNREACHABLE.json` confirms the scorer cannot reach `oos_worker.py`.
- [ ] `bringup_contract.json` declares the required scopes and the frozen readiness floors; ledger `schema_version=1` with per-component evidence and one smallest unblocking action per UNAVAILABLE component.
- [ ] Chromium sha256 matches and Playwright pinned to 1.63.0.
- [ ] No synthetic fallback code paths.
- [ ] `spec.json` and this `prereg.md` hashed into `freeze.json` before any episode runs.

---

**End of Preregistration**

This preregistration is frozen upon creation of `freeze.json`. No changes to hypothesis, arms, n, thresholds, decision rule or validity criteria are permitted after freeze. Any post-freeze change requires a new experiment ID. Operational retries of a frozen experiment must resume from the last valid checkpoint and must not rewrite frozen scientific inputs.
