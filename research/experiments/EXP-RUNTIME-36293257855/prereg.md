# Preregistration: EXP-RUNTIME-36293257855

## Lane: runtime
## Claim: C-MEAS-VALID (Measurement substrate is intervention-valid)
## Experiment ID: EXP-RUNTIME-36293257855

---

## 1. Strategic Question (from Global Research Director Mandate)

Now that the WAL-byte plus logical-projection plus response-fingerprint intervention oracle is VALIDATED against a planted surface on plain-HTTP, does that same oracle reach arm-constrained point sensitivity and specificity ≥ 0.90 with two-sided 95% Wilson lower bound ≥ 0.80 and non-degenerate intervals, when **BOTH** bounding confounds of the current scope are broken at once:

1. **AUTHORSHIP**: The intervention surface and its auth/session boundary are implemented in a module **separate from the scorer**, so the detector never shares an author with the ground-truth provider.

2. **TRANSPORT**: Episodes are driven through the **real Chromium browser** via Playwright public API (`p.chromium.executable_path` launch of the recorded chromium-1243 executable at sha256 `8c599d43aec53f2460a31ae2f4af6bd863f8258b34ff519564bc5d4726bfaa1e`, Playwright 1.63.0 via pip, real 1280×720 CDP DOM plus `Accessibility.getFullAXTree`) instead of the plain-HTTP client path, with **real button clicks as the ONLY write mechanism**, mandatory before/after WAL byte evidence, and **no synthetic fallback**.

---

## 2. Hypothesis

The composite intervention oracle (WAL-byte vector hash + SQL logical projection + stable-header response fingerprint) maintains arm-constrained discrimination (point sensitivity/specificity ≥ 0.90, Wilson 95% lower bound ≥ 0.80, non-degenerate confidence intervals) when:

- (a) The intervention surface and auth/session boundary are authored in a separate module from the scorer.
- (b) Episodes execute through a real Chromium browser via Playwright public API with real button clicks, rather than through the plain-HTTP client.

---

## 3. Falsifier

**Any** of the following constitutes falsification:

- Any of the six arms (P-WRITE, P-DRIFT, N-READ, N-INVALID, N-EXPIRED, N-DELETED) yields:
  - Point sensitivity/specificity < 0.90, **OR**
  - Wilson 95% lower bound < 0.80, **OR**
  - Degenerate confidence interval (ci_hi ≤ ci_lo).

- The positive-control planted intervention (PC-BROWSER-WRITE-PLANTED) fails to be detected (sensitivity < 1.0).

- Any null-control arm (NC-BROWSER-NULL-MATRIX) yields a false positive (specificity < 1.0).

- Independent recomputation check yields `zero_mismatches = false`.

- Capability ledger required scope FAIL.

---

## 4. Baseline (Validated Reference)

**B-PLAIN-HTTP-VALIDATED** — from EXP-RUNTIME-36129163700 Part A:
- 6 arms × 20 episodes = 120 episodes.
- All arms: point = 1.0, Wilson95 = [0.8388748419471806, 1.0], all intervals non-degenerate.
- Arm-blind detector, independent recomputation: zero mismatches.
- Substrate: 2× gunicorn 23.0.0 at 127.0.0.1:19860/19861 sharing `/tmp/single.db` SQLite WAL (`wal_autocheckpoint=0`), behind exclusive nginx 1.24.0 at 127.0.0.1:19851 with one `hash $request_uri consistent` upstream, real `proxy_cache`, authorization bypass, `X-Worker-Pid`.
- Plain HTTP on localhost, Python 3.12.14, Flask 3.1.3, PyJWT 2.15.0, Gunicorn 23.0.0, Playwright 1.63.0.
- Seed: 36129163700.

This baseline is **frozen** and will not be re-measured. It establishes the ceiling the new condition must meet.

---

## 5. Experimental Design

### 5.1 Arms (6 arms, 20 episodes each = 120 episodes total)

| Arm | Type | Auth State | Action | Expected WAL Mutation | Episodes |
|-----|------|------------|--------|----------------------|----------|
| P-WRITE | Positive | Valid-auth | Button click → server UPDATE | **Yes** (planted) | 20 |
| P-DRIFT | Positive | Valid-auth | Button click → representation change | **Yes** (planted drift) | 20 |
| N-READ | Null | Valid-auth | Read-only navigation | No | 20 |
| N-INVALID | Null | Invalid token | Button click (rejected) | No | 20 |
| N-EXPIRED | Null | Expired token | Button click (rejected) | No | 20 |
| N-DELETED | Null | Deleted session | Button click (rejected) | No | 20 |

### 5.2 Positive Control: PC-BROWSER-WRITE-PLANTED

- **P-WRITE arm** serves as the positive control.
- Each episode: valid-auth session, real button click on SPA write endpoint.
- Intervention surface (separate module) records the expected logical projection change.
- Server-side UPDATE mutates the WAL.
- **Required**: detector sensitivity = 1.0 (all 20 detected).

### 5.3 Null Control: NC-BROWSER-NULL-MATRIX

- Four arms: N-READ, N-INVALID, N-EXPIRED, N-DELETED.
- Each executed through Chromium with real button clicks (or navigation for N-READ).
- **Required**: detector specificity = 1.0 (0 false positives across all 80 null episodes).

---

## 6. Authorship Separation (Mandatory)

### 6.1 Intervention Surface Module
**Path**: `research/runtime/intervention_surface.py`

**Responsibilities** (and ONLY these):
- Flask app factory (`create_app()`).
- Routes: `/api/profile`, `/api/data_list`, `/runtime/write`, `/runtime/restore`, `/runtime/set_representation`.
- Auth/session boundary: `_authenticate()`, token validation, session lookup, 401/403 responses.
- WAL schema: `single.db` with `wal_autocheckpoint=0`, controlled row, logical projection.
- Ground-truth recording: expected logical projection per episode, planted values.

**Must NOT import**: `oracle_scorer.py` or any detector code.

### 6.2 Oracle Scorer Module
**Path**: `research/runtime/oracle_scorer.py`

**Responsibilities** (and ONLY these):
- WAL byte vector capture: length-framed SHA-256 over `/tmp/single.db` + `/tmp/single.db-wal`.
- Logical projection extraction: SQL query of controlled row.
- Response fingerprint: stable headers (excluding `Date`, `Server`, `X-Request-Id`).
- Composite detection: `detected = (wal_changed OR logical_changed OR fingerprint_changed)`.
- Arm-blind scoring: runs on episodes **before** arm labels are joined.
- Wilson score interval computation (two-sided 95%).
- Independent recomputation entry point.

**Must NOT import**: `intervention_surface.py` or any Flask/app code.

### 6.3 Harness / Orchestration
**Path**: `research/experiments/EXP-RUNTIME-36293257855/run_experiment.py`

- Imports **both** modules but contains **no** intervention logic or detection logic.
- Orchestrates: bring-up → episode loop → capture → score → record.
- Repairs the `pre_null_logical` NameError from EXP-RUNTIME-36129163700 (line 1444) **before freeze**.

---

## 7. Transport: Real Chromium via Playwright Public API

### 7.1 Browser Provisioning
- `playwright 1.63.0` via pip.
- `p.chromium.executable_path` resolves to:
  `/home/runner/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome`
- **Recorded sha256**: `8c599d43aec53f2460a31ae2f4af6bd863f8258b34ff519564bc5d4726bfaa1e`
- Browser version: `153.0.8010.12`
- Viewport: `1280×720` (actual, not requested).

### 7.2 Per-Episode Capture (inside measured interval)
1. Navigate to episode URL (valid-auth or null-auth as per arm).
2. **50 ms quiescence**.
3. Capture **before** WAL vector hash.
4. Capture **before** CDP DOM snapshot: `DOM.getDocument(depth=-1, pierce=True)`.
5. Capture **before** Accessibility tree: `Accessibility.getFullAXTree()`.
6. **Execute action**:
   - P-WRITE / P-DRIFT / N-INVALID / N-EXPIRED / N-DELETED: `page.locator('button[data-testid="write-btn"]').click()` (real button click).
   - N-READ: navigation only (no click).
7. **Wait for network idle** + **50 ms quiescence**.
8. Capture **after** WAL vector hash.
9. Capture **after** CDP DOM snapshot.
10. Capture **after** Accessibility tree.
11. Record response headers (stable set) and status.

### 7.3 No Synthetic Fallback
- Any failure in browser launch, navigation, click, CDP capture, AX capture, or WAL capture → record `UNAVAILABLE` or `ERROR` with evidence and smallest unblocking action.
- **No** `httpx`/`requests` client fallback for any episode.
- **No** synthetic WAL vector, DOM, or AX tree substitution.

---

## 8. WAL Byte Evidence (Mandatory)

- **Vector definition**: Length-framed SHA-256 over concatenation of `/tmp/single.db` and `/tmp/single.db-wal` (both files fully read, length-prefixed).
- **Capture timing**: Inside measured interval, after 50 ms quiescence, fixture setup/teardown outside.
- **Evidence artifact**: `artifacts/A-WAL-VECTOR-BEFORE-AFTER.jsonl` — 120 arm-blind records with `episode_id`, `arm`, `before_hash`, `after_hash`, `wal_changed` (boolean).
- **Stability control**: 10 no-action pairs (valid-auth, no click) → `artifacts/A-CAPTURE-STABILITY.jsonl` — all 10 must be byte-identical.

---

## 9. Arm-Blind Scoring & Independent Recomputation

### 9.1 Episode Order
- Pre-seeded RNG (recorded seed) generates episode order.
- Archived **before** any episode runs: `artifacts/A-SEEDED-ORDER.json`.

### 9.2 Detector Output (Arm-Blind)
- Detector runs on all 120 episodes **without** arm labels.
- Output: `artifacts/A-DETECTOR-OUTPUT.jsonl` — `episode_id`, `detected`, `wal_changed`, `logical_changed`, `fingerprint_changed`.

### 9.3 Label Join & Metrics
- Arm labels joined **after** detector output is written.
- Per-arm sensitivity/specificity with Wilson 95% CI (two-sided).
- All intervals must be non-degenerate (ci_hi > ci_lo).

### 9.4 Independent Recomputation
- Separate script reads **only** raw JSONL (`A-WAL-VECTOR-BEFORE-AFTER.jsonl`, `A-DETECTOR-OUTPUT.jsonl`, `A-SEEDED-ORDER.json`).
- Shares **no code** with producer scorer.
- Output: `artifacts/A-RECOMPUTE-CHECK.json` — `zero_mismatches` (boolean), mismatch details if any.
- **Required**: `zero_mismatches = true`.

---

## 10. Capability Ledger & One-Command Bring-Up

### 10.1 Bring-Up Contract
- **Path**: `research/runtime/bringup.py` + `bringup_contract.json`.
- **Command**: `python -m research.runtime.bringup --config research/experiments/EXP-RUNTIME-36293257855/bringup_contract.json --ledger .../artifacts/capability_ledger.json`
- **Exit code 0** + `OK: all declared required scopes pass` required before any episode runs.

### 10.2 Required Scopes (Must PASS)
| Scope | Description |
|-------|-------------|
| CAP-CHROMIUM-LAUNCH | Playwright public API launches canonical Chromium, captures DOM+AX |
| CAP-WAL-SUBSTRATE | 2× gunicorn + exclusive nginx + shared SQLite WAL, all floors met |
| CAP-NGINX-PROXY | nginx upstream `hash $request_uri consistent`, `proxy_cache`, MISS-then-HIT |

### 10.3 Explicitly UNAVAILABLE Scopes (Fail-Closed if Design Needs Them)
- BrowserGym (`import browsergym` → ModuleNotFoundError)
- AgentLab (`import agentlab` → ModuleNotFoundError)
- Policy-model credentials: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `HF_TOKEN`, `GITHUB_TOKEN` (all absent)
- GHCR (`https://ghcr.io/v2/` → HTTP 401)

### 10.4 Ledger Schema
- `schema_version: 1`
- Same-run identity, HEAD and worktree provenance.
- Redacted credentials.
- Per-scope required-versus-advisory classification.
- Exact commands, ports, WAL path and schema.
- Health checks, floors, evidence paths and hashes.
- Freshness timestamps.
- One smallest unblocking action per UNAVAILABLE component.

---

## 11. Decision Rule (Frozen)

| Outcome | Condition |
|---------|-----------|
| **SUPPORTS** | All 6 arms: point ≥ 0.90 ∧ wilson_lo ≥ 0.80 ∧ ci_hi > ci_lo. PC-BROWSER-WRITE-PLANTED sensitivity = 1.0. NC-BROWSER-NULL-MATRIX all 4 arms specificity = 1.0. Recomputation `zero_mismatches = true`. Capability ledger all required scopes PASS. |
| **FALSIFIES** | Any arm fails point ≥ 0.90 ∨ wilson_lo ≥ 0.80 ∨ ci_hi > ci_lo. OR PC sensitivity < 1.0. OR any NC arm specificity < 1.0. OR recomputation `zero_mismatches = false`. |
| **INCONCLUSIVE** | Infrastructure failure prevents completing 120 episodes. OR capability ledger required scope FAIL. OR mandatory WAL evidence missing for any episode. |
| **MEASUREMENT_INVALID** | Authorship separation violated (shared imports/module). OR synthetic fallback used for any failed probe. OR `pre_null_logical` NameError not repaired before freeze. OR detector shares code with intervention surface. OR WAL evidence captured outside measured interval. |

**No MIXED outcome** — this is a gate experiment with binary gate criteria.

---

## 12. Validity Threats & Mitigations

| Threat | Mitigation |
|--------|------------|
| Authorship leakage via shared constants/config | No shared imports. Any shared constants (e.g., WAL path) defined in a third `shared_config.py` imported by both, but **logic** remains separated. |
| Browser side-effects (cache, connection state) leaking into null arms | Each episode gets fresh browser context. Null arms execute real clicks/navigation; WAL capture proves no mutation. |
| Transient write-and-revert invisible to pre/post capture | 50 ms quiescence + fixture teardown outside interval. Stability control (10 no-action pairs) bounds risk. Not fully testable; acknowledged in `unknown`. |
| Representation drift (P-DRIFT) planted, not environmental | Acknowledged: drift detection demonstrated against planted drift only. Recorded in `unknown`. |
| Deterministic seed leakage across arms | Fresh per-case RNG with recorded seeds. Episode order pre-archived. |
| Estimator-id branching in code | No code path branches on estimator id. Single composite oracle only. |

---

## 13. Artifacts to Produce

| Path | Role | Description |
|------|------|-------------|
| `artifacts/A-WAL-VECTOR-BEFORE-AFTER.jsonl` | raw | 120 arm-blind pre/post WAL vector hashes |
| `artifacts/A-DETECTOR-OUTPUT.jsonl` | raw | Arm-blind detector output per episode |
| `artifacts/A-SEEDED-ORDER.json` | fixture | Pre-archived episode order |
| `artifacts/A-RECOMPUTE-CHECK.json` | derived | Independent recomputation result |
| `artifacts/A-CAPTURE-STABILITY.jsonl` | raw | 10 no-action byte-identical pairs |
| `artifacts/A-EPISODE-LEDGER.jsonl` | raw | 120 episodes with arm, token_class, http_status, planted value, pre/post logical |
| `artifacts/B-PLAYWRIGHT-CAPABILITY.json` | raw | Browser launch proof: executable path, sha256, version, viewport, DOM/AX capture |
| `artifacts/B-DOM-AX-CAPTURE.json` | raw | Sample DOM (28-node) + AX (30-node) captures |
| `artifacts/B-WAL-EVIDENCE.jsonl` | raw | Before/after WAL for browser write + restore + 4 nulls (created on failure branch too) |
| `artifacts/capability_ledger.json` | derived | 12-component fail-closed ledger |
| `artifacts/C-BRINGUP-CONTRACT.json` | derived | Bring-up contract execution record |

---

## 14. Product Consequences

### 14.1 If SUPPORTS (Positive)
- C-MEAS-VALID ceiling expands to **authorship-separated + real Chromium transport**.
- Downstream lanes (Graph: C-FRESHNESS, C-DELTA-REPAIR; Physics: statistical contract) **can preregister** "measurement-valid substrate" as a precondition.
- The one-command bring-up contract and capability ledger become **reusable, fail-closed prerequisites**.
- Runtime lane has delivered the transport/authorship boundary crossing — the single untested step blocking the program.

### 14.2 If FALSIFIES (Negative)
- C-MEAS-VALID **remains bounded** to plain-HTTP same-author scope.
- Downstream lanes **cannot inherit** the substrate as measurement-valid.
- C-FRESHNESS and C-DELTA-REPAIR remain stalled.
- Physics must certify statistical contract on a substrate that has not crossed the transport boundary.
- Program must either: (a) invest in hardening the transport/authorship boundary, or (b) accept the instrument is not portable and redesign the oracle for a narrower but transportable scope.

### 14.3 If INCONCLUSIVE / MEASUREMENT_INVALID
- Infrastructure or validity failure — **not a scientific result**.
- Exact failure recorded with smallest unblocking action.
- Experiment must be repaired and re-frozen; **no weakening of preregistration after seeing outcomes**.

---

## 15. Dependencies & Preconditions

1. **Global Research Director mandate** (present in `request.json`) — CONTINUE on C-MEAS-VALID.
2. **Parent handoff** (EXP-RUNTIME-36129163700) — carries forward established/rejected/unknown/do_not_assume.
3. **Chromium capability** — already demonstrated and hash-recorded in parent (artifacts/B-PLAYWRIGHT-CAPABILITY.json, B-DOM-AX-CAPTURE.json).
4. **Physics owns statistical contract certification** — Runtime must not duplicate.
5. **`pre_null_logical` NameError** — must be repaired in `run_experiment.py` **before freeze**.
6. **Durability** — frozen-scope implementation (intervention_surface.py, oracle_scorer.py, bringup.py, bringup_contract.json) must be HEAD-resident at freeze time.

---

## 16. Non-Goals (Explicitly Out of Scope)

- Production OAuth/OIDC (Keycloak), CDN, load-balancer, TLS, HTTP/2, multi-host.
- BrowserGym, AgentLab, policy-model integration.
- Cross-site transfer, LLM inheritance, semantic resolution.
- Generalizing beyond the 6-arm matrix or the planted intervention surface.
- Durability re-experiment (already satisfied at HEAD per parent handoff).

---

## 17. Seed & Determinism

- **Master seed**: `36293257855` (from experiment_id).
- Episode order: `random.Random(master_seed).shuffle(...)`.
- Per-episode RNG: `random.Random(master_seed + episode_index)`.
- All seeds recorded in `artifacts/A-SEEDED-ORDER.json` and provenance.

---

## 18. Freeze Checklist (Before Execution)

- [ ] `intervention_surface.py` and `oracle_scorer.py` exist with no cross-imports.
- [ ] `run_experiment.py` imports both but contains no intervention/detection logic.
- [ ] `pre_null_logical` NameError repaired (assigned inside four-nulls loop).
- [ ] `B-WAL-EVIDENCE.jsonl` write path created on failure branch.
- [ ] `bringup_contract.json` declares required scopes exactly as Section 10.2.
- [ ] Capability ledger `schema_version: 1` with all required fields.
- [ ] Chromium executable sha256 matches `8c599d43aec53f2460a31ae2f4af6bd863f8258b34ff519564bc5d4726bfaa1e`.
- [ ] Playwright version pinned to `1.63.0` in contract.
- [ ] No synthetic fallback code paths in `run_experiment.py`.
- [ ] Spec.json and this prereg.md hashed into `freeze.json` before any episode runs.

---

**End of Preregistration**

This preregistration is frozen upon creation of `freeze.json`. No changes to hypothesis, arms, thresholds, decision rule, or validity criteria are permitted after freeze. Any post-freeze change requires a new experiment ID.