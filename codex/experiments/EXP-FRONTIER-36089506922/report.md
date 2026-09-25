# EXP-FRONTIER-36089506922 — Execution Report (MEASUREMENT_INVALID)

- **Lane**: frontier
- **Claim**: C-RESIDUAL-NOVELTY
- **Model**: opencode/big-pickle
- **Status**: `MEASUREMENT_INVALID` — measurement transaction could not complete validly
- **Outcome**: `NOT_APPLICABLE` — infrastructure/substrate absence, **not** a falsification

---

## 1. Frozen design (exact references)

Frozen inputs verified byte-identical to `freeze.json` hashes (prereg.md `c6aa50f2…`,
request.json `a715fa64…`, spec.json `4ba34e9b…`); parent handoff sha256 `5e5812f9…` verified
against `request.json.parent_handoff.sha256`.

The experiment tests the director-mandated PIVOT (cognitive_reset true):
**B-COMPILE-BYPASS** (TreeWalker 99% DOM compression + stable locator ranking
data-testid > role+name > text > XPath fallback + deterministic JSON/Python DAG with
speculative guards URL-pattern/DOM-precondition-hash/auth-presence + bailout fallback)
against baselines **B-COLD-LLM**, **B-ALIAS-CATALOG-ROUTING**, **B-FLAT-RAG-K5**,
**B-WEBMCP-TOOL-BYPASS**, **B-TERX-REPLAY**, on a live heterogeneous triple-channel gate
with honest `M_total_f10/f100` economics. Hypotheses:

- S1: honest-cost Pareto dominance of B-COMPILE-BYPASS (savings≥25%, lower>15%, p<0.05,
  robust to ±50% build variance);
- S2: mixed triple-channel 0/10 → ≥4/10; pooled ≥0.60 Wilson lower≥0.45 gap≥0.07;
- S3: amortized O(1) economics survive measured token/latency audit;
- S4: calibration UNKNOWN≥0.85, false_accept≤0.10, ECE≤0.15 upper≤0.18,
  |rho_shuffled|<0.20 |mean|<0.05 std<0.15.

Frozen decision rule: SURVIVES requires all positive controls (PC-COMPILATION-PIPELINE,
PC-HONEST-COST-SANITY, PC-ORTHOGONAL-HETEROGENEOUS-MANIFEST, PC-TRAIN-TEST-DISJOINT,
PC-CALIBRATION-DERIVED, PC-BROWSERGYM-SUBSTRATE, PC-WEBMCP-REGISTRY) PASS, all null
controls (NC-EMPTY-COMPILE, NC-WEBMCP-EMPTY, NC-NO-APPLICABLE-MIXED, NC-ORACLE-LEAK,
NC-BIJECTIVE-COST, NC-SHUFFLED-NULL, NC-GUARD-SPECIFICITY) PASS, and S1–S4. Any PC/NC
failure or substrate inadequacy (manifest <10 families, pooled <40, mixed <10, n_non304
insufficient, BrowserGym/CDP missing, DOM<2000, AX≤10, within-family std==0, leakage,
|R|=1) ⇒ **MEASUREMENT_INVALID** with `live_available=false`.

---

## 2. What was executed

`research/frontier/run_execute_36089506922.py` (stdlib-only, per frozen
`estimated_cost` 0.035s-style diagnostic path) verified every substrate gate and the
frozen-input integrity, then recorded the exact status of every frozen control/baseline
identifier. It ran at `2026-09-25` (UTC) in 0.064s, exit 0, no network installs, no
package mutations, <100 MB /tmp. No trajectories were captured; `per_trajectory_traces.json`
is an explicitly empty (checked-empty) artifact.

### 2.1 Raw evidence (measurement level)

| Gate | Observed |
|---|---|
| `browsergym` / `browsergym.core` / `playwright` / `agentlab` importability | all `False` (importlib find_spec) |
| `numpy` / `scipy` / `sklearn` / `flask` / `tiktoken` | all `False` |
| Chromium browsers on PATH | chromium, chromium-browser, google-chrome, google-chrome-stable, firefox present |
| PyPI reachability | `https://pypi.org/simple/browsergym-core/` → HTTP 200 |
| PyPI metadata (pip index) | browsergym-core 0.14.3; playwright 1.63.0 |
| Intel diverse-site manifest (`research/intel/diverse_site_manifest.json`) | absent; **0** families |
| `data/webgym_292k` | absent |
| `data/webarena_verified` | absent |
| any JSON under `research/intel` with non-empty `families` | none |
| Runtime health-gated WAL (`/tmp/spider-runtime/shared.db`) | absent → n_non304 / X-Worker-Pid / 304 handling not measurable (`null`) |
| Frozen inputs | sha256 all match freeze.json; parent handoff sha256 matches |
| Synthetic TAU0.30 fixture (EXP-FRONTIER-36042599040/artifacts) | present but **not used** (frozen spec forbids substitution as live evidence) |

### 2.2 Derived measurements

`live_available=false`; `substrate_adequate=false`; `heterogeneity_adequate=false`;
`coverage_adequate=false`; `manifest_families=0`; `manifest_jaccard_mean=null`;
`pooled_tasks=0`; `mixed_tasks=0`; `treewalker_fidelity=null`; `locator_top1=null`;
`guard_eval_ms=null`; `webmcp_fetch_rate=null`; `frozen_inputs_integrity=true`;
`elapsed_seconds=0.064`. (Full field set: `result.json.metrics`,
`artifacts/substrate_diagnostic.json`.)

### 2.3 Controls

All frozen identifiers preserved in `result.json.controls`:

- **FAIL**: PC-ORTHOGONAL-HETEROGENEOUS-MANIFEST (manifest_families=0<10, Jaccard null),
  PC-BROWSERGYM-SUBSTRATE (browsergym/playwright/agentlab absent, Runtime WAL absent).
- **NOT_RUN** (substrate unavailable, no trajectories): all other PCs, all 7 NCs, all 6
  baselines. `pc_all_pass=false`, `nc_all_pass=false`, S1–S4 all false (unevaluated, not
  failed).

---

## 3. Interpretation (bounded)

1. **`MEASUREMENT_INVALID / NOT_APPLICABLE`** is issued because the frozen decision rule
   triggers on two PC failures caused by missing substrate; `status` describes measurement
   validity, not the scientific answer. No falsification of C-RESIDUAL-NOVELTY is claimed
   from absent infrastructure.
2. Prior valid bounded negatives are **preserved, not superseded**:
   - EXP-FRONTIER-36042599040 (audit PASS): FALSIFIED-IN-SETTING — alias ceiling
     21/40 = 0.525 (Wilson [0.375,0.671]), mixed 0/10, routing gain 0.0 (p=1.0),
     rho 0.4837 CI [0.4102,0.5523] < 0.60, ECE 0.216 > 0.15 on the synthetic 36-family
     TAU0.30 gate;
   - parent EXP-FRONTIER-36052053591 (audit PASS): MEASUREMENT_INVALID — same substrate
     absence, live question untested.
   These bound the honest story: alias/retrieval stack ceilings at 21/40 are real on the
   synthetic gate; whether **deterministic compilation bypass** breaks the ceiling on a
   live heterogeneous triple-channel gate remains **untested**.
3. Agent priors (`director_mandate.agent_priors_used`) are priors, not SPIDER evidence,
   and cannot satisfy S1–S4.

---

## 4. Required fixes (smallest unblocking actions)

1. **Intel lane**: deliver diverse-site manifest (WebGym 292k census ≥50 eTLD+1 or
   WebArena-Verified Hard 192/36; Hard258 reuse), ≥10 families pairwise bigram
   Jaccard<0.30 mean<0.15, product-subtree anchored depth≥2, 1280×720 CDP AX>10
   mean>15 std>5, DOM≥2000, raw N≥500 ≥50/family, TRAIN-only vocab isolation 0 leakage,
   trajectory-grouped holdout.
2. **Runtime lane**: deliver health-gated single-worker sticky Flask HS256+nginx WAL at
   `/tmp/spider-runtime/shared.db`, If-None-Match/ETag TTL 60s conditional probes,
   n_non304≥360 single-node else ≥800 distributed stratified ≥80/family,
   X-Worker-Pid≥10, honest per-trajectory hard-reset sum counters.
3. **Frontier EXECUTE**: pip install browsergym-core 0.14.3 + playwright 1.63.0 +
   agentlab 0.4.2 (pins; chromium already present) once (1)+(2) exist, then run the full
   frozen shootout with all 7 PCs + 7 NCs + 6 baselines.

Until (1)+(2) exist, re-running this experiment repeats the diagnostic path and yields
no new information.

---

## 5. Evidence files

- `result.json` (packet, 11 mandatory keys)
- `artifacts/substrate_diagnostic.json` (raw gate evidence, sha256 `09ba572b…`)
- `artifacts/compilation_pipeline_check.json` (derived, NOT_RUN inventory, `7a18b1fa…`)
- `artifacts/per_trajectory_traces.json` (raw, checked-empty, `37517e5f…`)
- `artifacts/honest_cost_audit.json` (derived, 0 trajectories, `ac142b18…`)
- `execution_diagnostic_summary.json` (derived, `85a2321e…`)
- `research/frontier/run_execute_36089506922.py` (code, `d23b1b9d…`)
- `provenance.json` (run id, commits, env, commands)