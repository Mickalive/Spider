# EXP-PRODUCT-35961222077 — Execute Report (Product REOPEN C-LLM-INHERIT)

**Status:** `MEASUREMENT_INVALID` — **Outcome:** `INCONCLUSIVE`  
(Infrastructure / measurement-gate failure per `EXPERIMENT_PACKET` §4/§9 — **not** scientific falsification of C-LLM-INHERIT.)

## 1. What ran (frozen checklist)

| Step | Result |
|------|--------|
| Frozen inputs | `request` `43a4574b` / `spec` `d2d2dce8` / `prereg` `bf9f9626` **MATCH** `freeze.json` after execute |
| Pins | gunicorn **23.0.0**, PyJWT **2.14.0**, Flask 3.1.3, nginx **1.24.0**, Python 3.12.14 — **PASS** |
| Kernel MV3/PC2 sub-gate | working-tree sha `d926279d`, **5/5 EXECUTABLE** conf 0.85, wrong-family UNKNOWN — **PASS** (uncommitted) |
| Single-node substrate | `/tmp/spider-runtime/shared.db` WAL, gunicorn single pid 69030, nginx `$request_uri` → `:18929`, HS256, INM **846/846**, `n_non304` **840** stratified **420/420** — **PASS** (substrate half of PC5) |
| Correlated probe | n0 304-hit **1.0**, n0.25 acc **1.0** stale 0.5 FA **0.0** saving **0.40**, random(seed42) acc **0.487**, delta **0.513** — diagnostics **PASS** |
| PC1 exact-repeat | **5/5** hit_rate **1.0**, per_hit 50 tok (file-proxy body/DOM hash disclosed) — **PASS** |
| PC2 holdout | **FAIL** — `value_set_A ∩ B ≠ ∅` on **18/36** even-index families (pool + usage); Jaccard 630 pairs max **0.0** PASS; kernel PASS; probe PASS; registry 714/2147 PASS |
| PC3 calibration | **PASS** non-vacuous: AUROC_true **0.919**, AUROC_null **0.482**, precision **0.968**, forced FA **0.169**∈[0.10,0.60], conf_std **0.453**, UNKNOWN_prec **0.983**, ECE **0.103** |
| PC4 formula+rho_proxy | **INCOMPLETE** — no dedicated 1e-6 audit file; `rho_proxy_real` **null** (no real tokens) |
| PC5 full | **FAIL** — substrate half PASS; Docker `ghcr.io/servicenow/browsergym:0.14.3` **denied**; `OPENAI_API_KEY` **ABSENT** → gpt-4o-mini 15-step **NOT RUN** |
| Fixtures | Hard258 **not** staged (pip `webarena` no dist); disclosed **192/36** fallback `391e8f6c` staged; qcr `8c69804b`; dsm **714/2147**; sgdr **36** (DOM-hash substituted, disclosed); cost_config `55fa25af` staged |
| NC1 shuffled | **FAIL degenerate**: `rho_shuffled=0.778` CI[0.709,0.830] **p=0.0002** (B=5000) ≥0.35 & p<0.01 |
| NC2 / NC3 | **PASS** AUROC 0.480 FA 0.104; rho_novelty 0.008 R² 4.3e-05 |
| Claim economics / margins | **null** — clause (1) fired before clause (3); **no** file-proxy surrogation for SURVIVES |

## 2. Decision-rule evaluation (frozen precedence)

**Clause (1) → MEASUREMENT_INVALID — multiple independent triggers:**

1. Docker BrowserGym 0.14.3 unavailable (GHCR `denied`, no local image, playwright missing).
2. `OPENAI_API_KEY` absent → gpt-4o-mini 15-step not run → `rho_proxy_real` unmeasurable.
3. **TRAIN contamination:** `value_set_A ∩ B ≠ ∅` on 18/36 fallback families → PC2/holdout fail (fixture **not** altered to force a pass).
4. PC2 composite **FAIL**; PC5 composite **FAIL** (LLM half).

**Clause (2) → also MEASUREMENT_INVALID:** NC1 null degeneracy `|rho_shuffled|=0.778 ≥ 0.35`, `p=0.0002 < 0.01`.

**Clause (3) / SUPERSEDE:** **Not reached.** Primary claim metrics remain `null` (unknown), not zero. Controls that did run (PC1/PC3/substrate/NC2/NC3/kernel) do not license FALSIFIED or SURVIVES for C-LLM-INHERIT.

## 3. Interpretation (distinct from observations)

No claim update is justified for **C-LLM-INHERIT**. The real-LLM inheritance question (SPIDER vs COLD / INSTRUCTIONS / RAG-k5 / Stagehand at margin ≥0.12, Pareto ≥25%, AUROC ≥0.75) remains **UNKNOWN**.

What *did* clear this run and can be inherited as bounded operational progress (not as claim validation):

- Single-node health-gated sticky HS256 substrate **actually provisioned and exercised** (`n_non304` 840 stratified, INM 100%, WAL single-worker) — the parent’s #1 blocker is now operationally solved for this path.
- Correlated ETag/TTL probe discriminates fresh vs stale vs seeded-42 random with large margin on that substrate.
- PC3 MockEnv calibration is non-vacuous (not a degenerate CI[1,1] or conf_std≤0.05 artifact).
- Kernel dot-regex working-tree patch still 5/5 (third replication); still **uncommitted**.

What remains blocking any SURVIVES/FALSIFIED reading: GHCR + OPENAI gates, a contamination-free holdout census, PC4 completion, and a non-degenerate NC1 shuffle redesign — **without** weakening frozen thresholds.

## 4. Smallest next actions (ordered)

1. **Holdout:** stage Hard258 if obtainable, else rebuild 192/36 (or odd-family-only 18) with `value_set_A ∩ B = ∅` on **all** families; re-run fixture_checks until `value_set_disjointness.pass=true`.
2. **Runtime gates:** authorize `ghcr.io/servicenow/browsergym:0.14.3` pull; provision `OPENAI_API_KEY`; keep substrate recipe (`run_experiment.py` provision path) as the single-node harness.
3. **NC1 fix (design, not thresholds):** repair shuffle so novelty–cost coupling is truly broken (current `n_eff=rng.random()` still leaves structure); re-preregister only via a new frozen design if NC definition changes.
4. **PC4:** emit dedicated formula-parity (≤1e-6) artifact + `rho_proxy_real` pooled/per-stratum once real tokens exist.
5. **Durability:** commit kernel dot-regex patch in product scope (currently worktree-only).
6. Re-execute **this same frozen design** after 1–2 clear; do not edit frozen `request`/`spec`/`prereg`.

## 5. Packet pointers

- Canonical: `result.json` (this run), `provenance.json`
- Raw/derived evidence: `artifacts/*` (hashes in `result.json.artifacts`)
- Fixtures staged: `fixtures/*` (byte-identical sources from EXP-PRODUCT-35916130502 except derived `sgdr_index_36.json`)
- Harness: `run_experiment.py` sha `bcd02459…`
