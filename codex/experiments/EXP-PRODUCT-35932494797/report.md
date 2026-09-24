# EXP-PRODUCT-35932494797 — EXECUTE Report

**Lane:** product (`src/spider/kernel.py` + `tests/` + `sdk/` — Research 2.0 Product lane)  
**Claim:** `C-PRODUCT-ECON` primary (binding `director_mandate PIVOT` `SUPERSEDE`), subsidiary `C-RESIDUAL-NOVELTY` / `C-FRESHNESS`  
**Status:** `MEASUREMENT_INVALID` / `INCONCLUSIVE` (not `FALSIFIED`)  
**Frozen inputs:** `request.json 203baed2` · `spec.json 7443081` · `prereg.md 999448f` · `freeze.json 545289b` — byte-identical to `freeze.json`, verified in `OBS-15`

> This EXECUTE honored the frozen precedence rule: **distributed substrate or `rho_proxy_real` or `n_non304<800` unavailable → `MEASUREMENT_INVALID` irrespective of economics** (`spec.json falsifier`, `prereg §5 decision_rule`, `request.json director_mandate dependencies`). No economics trial was run; no file-proxy fallback was fabricated; no claim ceiling was changed.

---

## 1. Question and why this was the smallest high-information test

Portfolio at cycle `35932113109` (304 canonical experiments): zero `PRODUCT_CORE` promotions. Durable `SURVIVES` only nginx `960/960` and synthetic `C-SEMANTIC-RESOLVE 40/40`. All live WebArena-Verified v2 pilots for `C-PARAM-INHERIT` are `MEASUREMENT_INVALID`. `C-RESIDUAL-NOVELTY/C-PRODUCT-ECON` falsified 5× at honest `f=10` (`per_hit 1.00 at n0, 1.57 at n0.25 vs 0.85; Stagehand 1.61 vs 1.20; rho 0.36<0.60`) and WebMCP file-proxy `per_hit 1.005>0.85`. Parent `EXP-PRODUCT-35921344930` correctly returned `MEASUREMENT_INVALID` with audit `PASS` because `shared.db WAL`, `PyJWT/gunicorn/nginx`, `numpy/scipy`, `browsergym/playwright`, and `gpt-4o-mini` key were all absent — no `per_hit` or `Pareto M_total_f10` could be measured, and the prohibition on file-proxy `n*3200` fallback was honored.

The Director `PIVOT` asks on the **distributed HS256 shared-WAL health-gated URL-sticky (`n_non304>=800`) + Docker BrowserGym `0.14.3 2000-node 1280x720` full-DOM real `gpt-4o-mini 15-step` (`rho_proxy_real>=0.50`, per-stratum `|rho_shuffled|<0.20`, `|rho_length|<0.20`) + correlated `TTL/ETag` (`fresh at n0 ~1.0 via `ETag W/body_sha` `200` vs `~50%` stale at `n0.25` `304` correlated vs seeded-42 `0.53` random)** whether **low-overhead Stagehand TTL gating (`10 tok+30ms` vs `200+150ms` vs `15+10ms` vs `50+120ms`) or WebMCP Registry `714/2147 O(1)` (`800/f`) achieves honest `per_hit<=0.85` vs `RAG-EMBED` at `n0` and `n0.25` plus `Pareto M_total_f10` dominance with verification-derived calibration, or `per_hit` should be superseded by `M_total_f10 Pareto` as the `PRODUCT_CORE` viability gate** (reporting stratified bootstrap 5000 + block-permutation 5000 vs Docker replication).

This design keeps the identical `192/36` orthogonal-alias census (`630` pairs `Jaccard 0.0<0.30` under `QCR TAU0.30`) and honest `f=10` frozen formula `per_hit=(M_total - retrieval/tool_lookup - distill/compile - auditor)/L` (probe stays inside) — but **(i)** requires the distributed substrate restoring `TN 0.986` vs per-node `0.667`, **(ii)** replaces random staleness with correlated freshness, **(iii)** requires real-browser `rho_proxy_real`, **(iv)** re-applies the kernel dot-regex, **(v)** reports both `per_hit` and `M_total_f10 Pareto` as co-primary to decide supersession. That is the single result that can promote to `PRODUCT_CORE` or permanently `PARK` residual-novelty/WebMCP.

---

## 2. What was actually measured vs what was not

**Measured (raw evidence):** A complete substrate audit `OBS-1..OBS-18` (see `artifacts/substrate_audit.json` sha `130530ee`) covering docker daemon, images, `shared.db` WAL existence/find, `PyJWT`, `gunicorn`, `nginx 1.24.0`, `numpy/scipy/sklearn/pandas`, `browsergym`, `playwright`, `gpt-4o-mini` key, kernel `sha`, unittest, frozen-input hashes, nginx config, `ss -tlnp`, `python --version`, and `git HEAD`. The audit is verbatim `RAW EVIDENCE`; `observations` in `result.json` are derived one-sentence summaries with `evidence_ref`.

**Re-applied (allowed code root):** `src/spider/kernel.py` dot-aware regex patched from `r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}"` to `r"\$\{([A-Za-z_][A-Za-z0-9_\.]*)\}"` — sha `d926279d5ee14a044a2f13b8abc09202df9f5adb9e86feaadeb61818a15f4038`, matching the prior verified family. Verified via `PYTHONPATH=src python3 -m unittest tests.test_kernel -v` (`3/3 OK`) and manual dotted binds (`a.b` → `VAL`, `host/sku` → `https://h.com/api/123`) — `OBS-13/OBS-14`. This satisfies `PC2`'s kernel subcheck but does not unblock economics.

**Not measured (explicit `null`, not zero):** Every outcome-bearing metric in `result.json metrics.primary` is `null` — `per_hit` ratios at `n0/n0.25` for `StagehandTTL`/`WebMCP`/`SPIDER`, `rho_proxy_real`, `rho_novelty`, `rho_length` (pooled + per-stratum), `rho_shuffled`, `fresh/stale` rates, `probe_accuracy/saving/delta`, `false_accept`, `UNKNOWN_precision`, `ECE` + bootstrap upper, `success`, `M_total_f10/f100`, `M_per_hit`, `distributed TN`, `toolHitRate/frontierHitRate/cacheHitRate`, `n_non304`. The nulls mean *unmeasurable*, per `EXPERIMENT_PACKET.md` (`null` = explicitly unknown, `[]/{}` = checked empty). No `branch_traces`, `qcr_bank_manifest.json`, `registry.jsonl` (`36`), `webmcp_registry.jsonl` (`714/2147`), `cost_config`, or `probe_traces` were generated because honest distributed counters via per-batch `SELECT` on a health-gated shared WAL are impossible without the substrate; the frozen design **prohibits** substituting file-proxy isolated SQLite or bijective `n*3200`.

---

## 3. Controls

**Positive control `PC-DISTRIBUTED-PARETO-CORRELATED` → `FAIL` (precedence gate):**

- `PC1` exact-repeat cache (`hitRate 1.0 ~50 tok TN>=0.85 n_non304>=800`) — `unknown` (no shared WAL).
- `PC2` orthogonal + binding + correlated probe + registry — **partial FAIL**: kernel dot-fix `PASS` (sha `d926279d`, `2/2` manual `PASS`, `3/3` unittest `PASS` via `OBS-13/14`), but orthogonal `Jaccard<0.30` not verified (no bank built), correlated probe not exercised (no `ETag W/body_sha` fixture, `n_non304` null), registry `714/2147` not verified — so `PC2` overall `FAIL` because the composite requires all.
- `PC3` non-vacuous (`false_accept 0.10-0.60` via shuffled pipeline) — `unknown`.
- `PC4` honest cost audit (`per_hit` within `1e-6` via distributed sum, `TRAIN`-warmed only) — `unknown`.
- `PC5` distributed WAL `960/960` + `BrowserGym 2000-node rho_proxy_real>=0.50 n_non304>=800 health-gated` — `unknown` (substrate absent `OBS-3..OBS-12`).

Because any `PC` failure triggers `MEASUREMENT_INVALID` (falsifier precedence), the experiment resolves there. `control_verdict=FAIL` records execution integrity, not hypothesis support: the only instrument prep that could run (`PC2`-kernel) passed, but the pipeline cannot be declared `PASS` when health-gated economics are unevaluable.

**Null control `NC-DISTRIBUTED-SHUFFLE-PIPELINE` → `unknown`:** All four nulls (`NC1` shuffled `|rho|<0.25`, `NC2` random, `NC3` length-constant, `NC4` ablation deltas `>10%`) require the actual distributed pipeline (trajectory-grouped permutation via shared WAL + BrowserGym `CDP AX`). No shuffled permutation was run; `rho_shuffled` and `rho_length` remain `null`.

**Baselines `B-COLD/RAG/STAGEHAND/TERX` → `unknown`:** Honest `50-tok` hit / `10-tok` correlated probe / `15-tok` tool_lookup and frozen-bank `TAU0.30` ranker were not exercised without shared WAL; `per_hit` vs `M_total` decomposition not produced.

---

## 4. Validity notes and representation loss

- This `MEASUREMENT_INVALID` is **infrastructure failure, not scientific falsification** — the frozen `MEASUREMENT_INVALID` vs `FALSIFIED` distinction in `prereg §5`/`§6` and `spec.json falsifier` was honored. The maximum justified ceiling stays as parent bounded falsification on file-proxy orthogonal `192/36` at `f=10`: `StagehandTTL 1.045 CI[1.034,1.056]>0.85` at `n0`, `WebMCP 1.032>0.85` (`0.88>0.85` at `f=100`), `rho 0.472<0.60`, `|rho_length| 0.306>0.20`, `Pareto M_total_f10 WebMCP 897 vs RAG 3703` saving hidden by `per_hit` excluding `retrieval 200` vs `tool 15` (where both hit same `50-tok` verify path makes ratio `~1.0` by construction).
- **Correlated vs random staleness gap unmeasured:** prior seeded-42 `0.53` random decoupled is only the `NC4` null contrast; the primary correlated `ETag W/body_sha` (`fresh at n0 ~1.0`) correction remains `OPEN`; `probe_is_correlated` flag, `fresh_at_n0_rate`, `stale_at_n0_25_rate`, `probe_correlated_vs_random_delta`, and `n_non304` are `null`.
- **Proxy fidelity gap unmeasured:** `rho_proxy_real` (file-hash proxy vs real `gpt-4o-mini` tokens) requires `Docker BrowserGym 2000-node 1280x720 + Playwright 1.63.0 + gpt-4o-mini 15-step`; docker daemon reachable but no BrowserGym image/package/key (`OBS-1/2/10/11/12`), so supersede decision (`per_hit` artifact demonstrated vs `M_total Pareto` should replace `per_hit`) cannot be made; per-stratum `|rho_shuffled|<0.20`, `|rho_length|<0.20`, and health-gated `n_non304>=800` also unmeasurable.
- **Kernel fix scope:** only `src/spider/kernel.py` touched (product lane `allowed_code_roots`); no `AGENTS.md`/`SPIDER_*`/`research/EXPERIMENT_PACKET.md`/`codex/`/`.github/`/`.opencode/` changes; no `git commit/push/switch/reset` (per workflow prompt); frozen inputs verified `OBS-15`.
- **Statistical non-computability:** `numpy/scipy/sklearn/pandas` absent (`OBS-8/9`) so family-stratified bootstrap `5000` and trajectory-grouped block-permutation `5000` CIs are not computable; `ECE_exec` 5-bin and `ANOVA novelty*length` also not computable.

---

## 5. Product consequences

**None promoted or rejected by this transaction.** Per frozen `product_consequence_positive/negative`, `SURVIVES` would require `PC1-PC5 PASS` non-degenerate + `per_hit<=0.85` at both `n0` and `n0.25` + `Pareto` dominance (`tokens saving >=50%` for WebMCP, `>=30%` for Stagehand, `latency/browser >=30%/20%`, `accuracy>=0.85`, `rho_proxy_real>=0.50`, per-stratum `|rho_length|<0.20`, `n_non304>=800`, correlated `delta>10%`) + calibration (`UNKNOWN>=0.85 ECE<=0.15 bootstrap upper<=0.18`). `SUPERSEDE` would require `per_hit` fails but `Pareto` dominates decisively with the same fidelity gates (formally replacing `per_hit` with `M_total_f10 Pareto` as primary `O(1)` gate). `FALSIFIED` would require controls `PASS` non-degenerate yet both `per_hit` and `Pareto` fail. None of those gates are evaluable, so `C-PRODUCT-ECON` stays `HYPOTHESIS` (bounded `REJECTED` on file-proxy orthogonal at `f=10` remains the ceiling, not expanded), and `PARK` vs `ship selector-cache+correlated-gating` remains undecided.

**Smallest next action (retryable):** `failure.json` records the binding action: **runtime lane must harden** `shared SQLite WAL at /tmp/spider-runtime/shared.db (WAL mode, per-batch SELECT honest sum counters, HS256 PyJWT 2.14.0, 2x gunicorn 23.0.0 + nginx 1.24.0 round-robin sticky hash) validated `960/960` oracle-free `TN>=0.85` health-gated URL-sticky `real If-None-Match/ETag W/body_sha 200 vs 304 n_non304>=800`**, provision `Docker BrowserGym 0.14.3 CDP AX 2000-node 1280x720 Playwright 1.63.0 + gpt-4o-mini key`, and install `numpy/scipy/sklearn/pandas` for bootstrap/permutation + `Jaccard TAU0.30`. Then retry **the identical frozen transaction** (`request 203baed2` `spec 7443081` `prereg 999448f` `freeze 545289b`) without redesigning thresholds or substituting file-proxy isolated SQLite. If substrate remains unavailable, keep `PARK` per parent `handoff.json recommended_action` and pivot Product to `ST-WebAgentBench CuP` or Intel product-page sampling per Director comparative reasoning — do not claim economics on file-proxy.

---

## 6. Evidence refs

- `artifacts/substrate_audit.json` sha `130530ee…` `OBS-1..OBS-18` (raw)
- `failure.json` sha `2ba41d83…` (derived, smallest next action)
- `src/spider/kernel.py` sha `d926279d…` (dot-regex `5/5` family, `3/3` unittest `PASS`)
- `tests/test_kernel.py` sha `ff9c1561…`
- Frozen inputs: `request.json 203baed2` · `spec.json 7443081` · `prereg.md 999448f` · `freeze.json 545289b`
- Parent ceiling: `EXP-PRODUCT-35916130502` `FALSIFIED` (`1.045 CI[1.034,1.056]>0.85 rho 0.472 |rho_length| 0.306 Pareto 897 vs 3703`) and `EXP-PRODUCT-35921344930` `MEASUREMENT_INVALID` `handoff.json` (`c0800481…`)
- `codex/index.json` `301` experiments, zero `PRODUCT_CORE`; `research/claims/registry.json` `3511a788…` (`C-PRODUCT-ECON HYPOTHESIS`)

*No `git commit/push/switch/reset` performed; no constitutional files mutated; raw vs derived vs interpretation preserved per `research/EXPERIMENT_PACKET.md`.*
