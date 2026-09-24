# EXP-PRODUCT-35936223443 — Execution Report

**Lane:** product — `src/spider/kernel.py` + `tests/` + `sdk/` (Research 2.0 Product lane)  
**Claim:** `C-PRODUCT-ECON` (primary, `director_mandate PIVOT` with `cognitive_reset true`) — subsidiary `C-RESIDUAL-NOVELTY`, `C-FRESHNESS`  
**Status:** `MEASUREMENT_INVALID` / `INCONCLUSIVE` — not a scientific negative  
**Executed:** 2026-09-24T00:04:00+00:00 — 2026-09-24T00:07:00+00:00  
**GitHub Run:** `35936223443` (attempt 1)  
**Base SHA:** `c2b97ca249252ee1fd709de96d916f8e51ed89b4` → Pre-execute `bedd6205772d04b36aff76b7f57190f5d9382c95` → Post-execute `8dccde1c6b121866766f1b2f9bbb6d7b4ea57612` (uncommitted kernel patch only)  
**Frozen Inputs:** `request.json` `a3532d5d` / `spec.json` `b4403f1b` / `prereg.md` `c64f2b23` / `freeze.json` `6e75efa3` — byte-identical to freeze (substrate_audit OBS-14)  
**Artifacts:** `artifacts/substrate_audit.json` `af30657e` (raw), `failure.json` `67060af7` (derived), `src/spider/kernel.py` `d926279d` (code), `tests/test_kernel.py` `ff9c1561` (code)

---

## 1. Summary — Measurement Invalid, Not Falsified

This execution correctly enforces the frozen `spec.json:falsifier` precedence and `prereg.md` §5 decision rule:

> `PC failure or degenerate CI or frontier/registry artifact or distributed substrate unavailable/single-worker sticky violated or n_non304<800 or If-None-Match not exercised or health-gate failed → MEASUREMENT_INVALID irrespective of economics`

All four blocking substrate sub-conditions are simultaneously violated (see §3 raw audit). Per `EXPERIMENT_PACKET.md` §1 mandatory-key semantics, infrastructure absence is encoded as `null` primary metrics with `validity_notes` explanation, not as zero or as `FALSIFIES`. The companion `failure.json` records the `BLOCKED` category and smallest next action (runtime hardening).

**No outcome-bearing economics census was run.** Honoring the frozen prohibition on file-proxy isolated SQLite fallback (prereg §4, spec `measurement_validity[3]`), this experiment did **not** fabricate a `~2600` trial `n*3200` or `192/36` file-proxy run. The only instrument preparation that survived is the durable kernel dot-regex patch (see §2). Consequently:

- `result.json:metrics.primary` — all 40+ per_hit / Pareto / rho / calibration metrics are explicit `null` (unmeasurable, not zero).
- `result.json:controls` — `PC-DISTRIBUTED-PARETO-CORRELATED-SINGLE` `fail` (kernel subcheck `PASS`, all other subchecks `unknown`), `NC-DISTRIBUTED-SHUFFLE-PIPELINE-SINGLE` `unknown`, all 7 baselines (`B-COLD`, `B-RAG-EMBED`, `B-STAGEHAND-CACHE`, `B-TERX-REPLAY`, `P-STAGEHAND-TTL`, `P-WEBMCP-TOOL`, `P-SPIDER-MEA-BATCHED`) `unknown`.
- `result.json:control_verdict` — `FAIL` scopes to execution integrity (PC precedence gate), while audit-style validity is preserved as infrastructure failure.
- Maximum justified economics ceiling remains the **parent bounded falsification on file-proxy only** (see carry_forward below) — no new ceiling established this transaction.

---

## 2. Question, Hypothesis, Falsifier (Frozen)

**Question (spec.json verbatim):**

> On distributed HS256 shared-WAL substrate (health-gated URL-sticky `$request_uri` If-None-Match/ETag->304 `n_non304>=800`, single-worker sticky) with Docker BrowserGym 0.14.3 2000-node 1280x720 full-DOM real `gpt-4o-mini` 15-step tokens/browser+latency (`rho_proxy_real>=0.50`, `|rho_shuffled|<0.20` per-stratum `|rho_length|<0.20`) and correlated TTL 60s max-age conditional probe ETag `W/body_sha` `~50%` stale at `n0.25` vs `~1.0` at `n0`, does Stagehand selector-cache + TTL gating vs WebMCP Registry 714 sites/2147 tools O(1) compilation (amortized compile `800/f`) achieve honest `per_hit=(M_total_f10 - retrieval - distill_or_compile_amort - auditor_amort)/L <=0.85` vs RAG-EMBED at `n0/n0.25` and `<=1.20` vs Stagehand HIT at `n0` and Pareto `M_total_f10` dominance (tokens vs browser+latency vs accuracy) with verification-derived calibration `false_accept<=0.10 UNKNOWN precision>=0.85 ECE<=0.15 bootstrap upper<=0.18`, or should `per_hit` be formally superseded by `M_total_f10` Pareto as PRODUCT_CORE gate, reporting family-stratified 5000 bootstrap + block-permutation 5000 vs `gpt-4o-mini+Playwright` replication?

**Hypothesis:**

Distributed correlated freshness `single-worker sticky` health-gated `$request_uri` is the single missing prerequisite that bounded per_hit FALSIFICATION (`Stagehand 1.045 CI[1.034,1.056]>0.85 rho 0.472<0.60 seeded-42 0.53 random decoupled`) to file-proxy. On distributed `HS256 shared-WAL single-worker sticky` health-gated `URL-sticky $request_uri` plus Docker `BrowserGym 2000-node 1280x720` full-DOM with real `gpt-4o-mini` where `rho_proxy_real>=0.50` and per-stratum `|rho_shuffled|<0.20 |rho_length|<0.20` and `n_non304>=800` `single-worker sticky`, a correlated conditional probe (`ETag W/body_sha max-age 60`: fresh at `n0 ~1.0` `n_non304` vs `~50%` stale at `n0.25` `304` correlated) will make Stagehand TTL gating (`10 tok+30ms` vs `200+150ms` vs `15+10ms` vs `50+120ms` fallback `health-gated $request_uri single-worker sticky`) achieve honest `per_hit<=0.85 vs RAG at n0 AND n0.25` and `Pareto M_total_f10` dominance with verification-derived calibration (`UNKNOWN>=0.85 ECE<=0.15` `n_non304>=800` `single-worker sticky`), OR if `per_hit` still `>0.85` despite correlated freshness but `M_total_f10 Pareto` shows decisive total-cost dominance with `rho_proxy_real>=0.50` `n_non304>=800` `single-worker sticky` then `per_hit` is artifact and should be superseded.

**Falsifier Precedence (spec.json):**

1. `PC failure` or degenerate CI or frontier/registry artifact or **distributed substrate unavailable/single-worker sticky violated or `n_non304<800` or `If-None-Match` not exercised or health-gate failed → `MEASUREMENT_INVALID`** irrespective of economics;
2. else `|rho_shuffled|>=0.35 p<0.01` leak or test-warmed cache/registry/probe or bijective `n*3200` or per-node `TN 0.667` artifact → `MEASUREMENT_INVALID`;
3. else economics/calibration/Pareto gate: `F1` `StagehandTTL/RAG>0.85` at `n0` OR `n0.25`, `F2` `WebMCP/RAG>0.85` at `n0 AND n0.25 f=10`, `F3` calibration fail, `F4` correlated freshness fail, `F5` `rho_proxy_real<0.50` or per-stratum `|rho_length|>=0.20` → `FALSIFIED` or `SUPERSEDE` if Pareto dominates decisively (≥50% token saving WebMCP / ≥30% Stagehand + latency/browser thresholds + `accuracy>=0.85` + `rho_proxy_real>=0.50` + per-stratum `|rho_length|<0.20` + `n_non304>=800` + correlated vs random delta `>10%`).

**Decision Rule (spec.json summary):**

All thresholds family-stratified pooled `N~192` on **distributed HS256 shared-WAL health-gated URL-sticky `$request_uri` `n_non304>=800` single-worker sticky + Docker BrowserGym 2000-node 1280x720** `f=10` honest sum counters; `SURVIVES_CURRENT_TEST` iff `C1` correctness+calibration + `C2` positive controls (`PC1`+`PC2`+`PC5`+`PC3`+`PC4`) + `C3` economics (`<=0.85` at both `n0` and `n0.25`, `<=1.20` vs StagehandCache, `<1.0` vs TERX) + `C4` Pareto dominance + `C5` `rho>=0.50` with per-stratum `|rho_length|<0.20 |rho_shuffled|<0.20 rho_proxy_real>=0.50 n_non304>=800`; `SUPERSEDE` if `C1+C2+C5` PASS but `C3` fails and `C4` Pareto dominates; `FALSIFIED` if `C3`/`C4` fail together with `C2` PASS and Pareto not dominant; **`MEASUREMENT_INVALID` if any `PC` fails (including `TN<0.85` or `rho_proxy_real` unmeasured or `n_non304<800` or census not orthogonal or probe not correlated) — this gate correctly fired.**

---

## 3. Raw Substrate Audit — 19 Observations (RAW EVIDENCE)

Full machine-readable audit: `artifacts/substrate_audit.json` `af30657e` (19 entries, each with `raw_evidence` string). Key excerpts (observations distinct from interpretation):

| ID | Observation (raw) | Evidence |
|---|---|---|
| OBS-1 | docker daemon reachable, 0 running containers | `docker ps` empty, exit 0 |
| OBS-2 | No BrowserGym/WebArena Docker images; only `gh-aw-*`, `github-mcp-server`, `dependabot` | `docker images` list |
| OBS-3 | No shared WAL at canonical paths | `/tmp/spider-runtime/shared.db exists=False`; `/tmp/spider-runtime-35936223443/shared.db exists=False` |
| OBS-4 | `find /tmp -name shared.db` empty (only `Permission denied` on `systemd-private/*`) | find exit 0 |
| OBS-5 | PyJWT not installed | `import jwt` → `No module named 'jwt'` |
| OBS-6 | gunicorn 23.0.0 not installed | `gunicorn --version` not found; `pip show gunicorn` `Package(s) not found` |
| OBS-7 | nginx binary present `1.24.0` at `/usr/sbin/nginx` but **no upstream** | `nginx -v` → `nginx/1.24.0 (Ubuntu)`; config default http block only |
| OBS-8 | numpy not installed | `import numpy` → `No module named 'numpy'` → `bootstrap5000_computable false` |
| OBS-9 | scipy, sklearn, pandas all not installed | `No module named 'scipy/sklearn/pandas'` |
| OBS-10 | BrowserGym 0.14.3 python package not installed | `import browsergym` → `No module named 'browsergym'` |
| OBS-11 | playwright not installed | `import playwright` → `No module named 'playwright'` |
| OBS-12 | No `gpt-4o-mini` API key in env | `OPENAI_API_KEY / GPT4O_MINI_KEY / OPENAI_KEY / ANTHROPIC_API_KEY` all `False` |
| OBS-13/19 | **Kernel dot-regex re-applied and verified**: pre-patch `46929b3a` non-dot `r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}"` → post-patch `d926279d5ee14a044a2f13b8abc09202df9f5adb9e86feaadeb61818a15f4038` dot-aware `r"\$\{([A-Za-z_][A-Za-z0-9_\.]*)\}"`; `3/3` unittest PASS; manual dotted `_template_slots`/`_bind` `a.b` + `sku.id` `2/2` PASS | `src/spider/kernel.py` sha, `PYTHONPATH=src python3 -m unittest tests.test_kernel -v` |
| OBS-14 | Frozen inputs byte-identical to `freeze.json` | `request a3532d5d`, `spec b4403f1b`, `prereg c64f2b23` match `freeze.json` `6e75efa3` |
| OBS-15 | `n_non304` null, health-gated `false` | No shared WAL, no nginx upstream, no `HEAD If-None-Match ETag W/body_sha` probe exercised |
| OBS-16 | No outcome-bearing trial run (honors fallback prohibition) | No `branch_traces`/`qcr_bank_manifest.json`/`registry.jsonl`/`webmcp_registry.jsonl`/`cost_config.json`; no `n*3200`; honest `per-batch SELECT` not attempted |
| OBS-17 | `bootstrap 5000 / block-permutation 5000 not computable` | numpy/scipy absent |
| OBS-18 | nginx config no experiment upstream gunicorn workers | `/etc/nginx/nginx.conf` default http block only; `$request_uri` sticky hash not exercised |

**Environment:** Python `3.12.14`, Linux `6.17.0-1022-azure`, `sqlite3 3.45.1` isolated availability not used for distributed honesty (prohibited). All `OBS` preserved as raw strings in audit JSON; `result.json:observations` are condensed summaries referencing `evidence_ref`.

---

## 4. Kernel Binding Fix — Durable Prep (Only Code Change)

**Allowed roots:** product lane `src/`, `tests/`, `sdk/`, `pyproject.toml` per `research/lanes/registry.json`.

**Change:**

```
src/spider/kernel.py: _PARAMETER = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")
                   → _PARAMETER = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_\.]*)\}")
sha before: 46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61
sha after:  d926279d5ee14a044a2f13b8abc09202df9f5adb9e86feaadeb61818a15f4038 (1 insertion, dot in capture group)
```

**Rationale:** `prereg §4 Binding fix (re-apply, currently missing in HEAD)` — Current HEAD without dot is baseline; patched sha without dot was previously `d926279d` with dot and logged as required for `PC2` kernel binding `1.0/1.0 confidence>=0.80` via `5/5` per-family `n0` spot-check `EXECUTABLE` with correct `bound_action` via `kernel.resolve`. Provenance prior `d926279d` had dot.

**Testing (per `AGENTS.md` product discipline):**

```
PYTHONPATH=src python3 -m unittest tests.test_kernel -v
  test_invalidation_forces_abstention ... ok
  test_parameterized_mechanism_binds_only_when_guarded ... ok
  test_unknown_is_default ... ok
  Ran 3 tests in 0.002s OK
Manual dotted checks:
  _template_slots('${a.b}') → {'a.b'} PASS
  _template_slots('/api/items/${sku.id}/price') → {'sku.id'} PASS
  _bind('/api/${host.sku}', {'host.sku':'X'}) → '/api/X' PASS
  _bind('${sku.id}', {'sku.id':'B123'}) → 'B123' PASS
  Kernel resolve with dotted slots:
    Mechanism parameter_slots=['sku.id'] + template '/api/items/${sku.id}' → resolve EXECUTABLE + correct bound_action PASS (2/2)
```

No other files mutated; no `pyproject.toml`/`sdk` change; no git commit/push performed (branch/scope discipline).

---

## 5. Controls — Expected vs Observed

### Positive Control `PC-DISTRIBUTED-PARETO-CORRELATED-SINGLE` — `fail` (precedence gate)

**Expected (spec `positive_control`):**

- `PC1` `B-TERX`/`B-STAGEHAND` at `n0` exact-repeat `hitRate 1.0` `per_hit ~50` via shared WAL `TN>=0.85` health-gated `$request_uri` `n_non304>=800` single-worker sticky.
- `PC2` orthogonal `cross-family Jaccard<0.30` (`0/630 >=0.30`, max `0.0` `hitRate 0.387 at n1.0`) + kernel binding `1.0/1.0 confidence>=0.80` `5/5` via `kernel.resolve` + **correlated probe** `fresh at n0 ~1.0` (`200` `n_non304`) vs `~50%` stale `304` at `n0.25` `accuracy>=0.90 saving>=30% falseAccept<0.05` `ETag W/body_sha` health-gated `$request_uri` `n_non304>=800` vs seeded-42 random `0.53` null + WebMCP `714/2147 1.0 at n0 15 tok` via shared WAL `single-worker sticky`; `TRAIN`-warmed audit `blockRate 1.0` `cacheHit 0.70-0.85` `TN 0.986` vs per-node `0.667`.
- `PC3` non-vacuous `false_accept 0.10-0.60` via shuffled probe/registry via actual distributed pipeline health-gated `single-worker sticky` (MockEnv `p=0.15`).
- `PC4` honest cost audit: frozen `per_hit=(M_total - retrieval/tool_lookup - distill/compile - auditor)/L` within `1e-6` via honest distributed sum counters health-gated `single-worker sticky`, `rho_proxy_real>=0.50` per-stratum `|rho_shuffled|<0.20 |rho_length|<0.20` `n_non304>=800`.
- `PC5` distributed WAL `960/960` per-batch `SELECT` `HS256 PyJWT 2.14.0` `1x gunicorn 23.0.0 single-worker + nginx 1.24.0 $request_uri sticky` health-gated `200 vs 304` `TN>=0.85` + BrowserGym `2000-node 1280x720` `rho_proxy_real>=0.50`.

**Observed:**

- `PC2-kernel` subcheck `PASS` (see §4): dot-regex sha `d926279d`, `3/3` unittest, `2/2` manual dotted `PASS`.
- `PC1`, `PC3`, `PC4`, `PC5` subchecks `unknown` (not evaluable): shared WAL absent `OBS-3/4`, PyJWT/gunicorn absent `OBS-5/6`, nginx no upstream `OBS-7/18`, BrowserGym/Playwright absent `OBS-10/11`, gpt key absent `OBS-12`, `n_non304` null `OBS-15`, `bootstrap` absent `OBS-17`, no `960/960` probe, no per-batch `SELECT`, no `ETag` probe `OBS-16`.
- `PC2` orthogonal `Jaccard` + correlated probe `fresh~1.0 vs stale~0.5` + WebMCP `714/2147` `status fail` (kernel `PASS` alone insufficient; bank/registry not generated).

Per frozen `decision_rule` precedence, any `PC` subcheck `fail` or `unknown` due to substrate absence triggers `MEASUREMENT_INVALID` — correctly enforced, not retried as `FALSIFIED`.

### Null Control `NC-DISTRIBUTED-SHUFFLE-PIPELINE-SINGLE` — `unknown`

**Expected:** Trajectory-grouped permutation of `parameter_slots` + TTL valid_key to seeded-42 random `0.53` decorrelated + WebMCP correct-site keys + frontier keys + randomize `probeHit/cacheHit/registryHit` via actual distributed pipeline health-gated `single-worker sticky` → `|rho|<0.25` n.s. (`|rho_shuffled|<0.20 p>=0.20` per-stratum `|rho_length|<0.20` within-family `std>0`) `success<=COLD` `false_accept 0.10-0.60` `UNKNOWN>=0.80` `crossFamily/toolFamily 0`; `NC2` random → `false_accept>=0.10`; `NC3` length-constant `L*500` → `|rho|<0.25 R2<0.15`; `NC4` ablations `correlated vs random delta>10%` `shared vs per-node TN 0.986 vs 0.667` `compile off vs on` etc. Correlated probe must **not** rescue shuffled.

**Observed:** `unknown` — all nulls require actual distributed pipeline (`resolve/_bind/probe/registry/frontier/MockEnv/auditorCache` via shared WAL + BrowserGym CDP AX hash) which is absent; no shuffled permutation `5000` run; no `rho_shuffled`/`rho_length` computed; no ablation deltas. Bootstrap uncomputable `OBS-17`.

### Baselines `B-*` / SUTs `P-*` — all `unknown` (not falsified)

| ID | Expected | Observed |
|---|---|---|
| `B-COLD` | flat `per_hit ~500` `M_total_f10 ~5497` tokens `latency ~7265ms` via shared WAL | not run — substrate absent |
| `B-RAG-EMBED` | `per_hit ~54.7 at n0` `M_total_f10 ~3703` `TFIDF TAU0.30 top-1` `200+150ms` via shared WAL | not run — frozen bank `TAU0.30` not exercised |
| `B-STAGEHAND-CACHE` | `hitRate 1.0 at n0 per_hit ~50 0 at n>=0.25` `DOM-hash 2000-node 1280x720` via shared WAL `TN>=0.85` `n_non304>=800` | not run |
| `B-TERX-REPLAY` | `per_hit ~50 at n0 ~500 at n>=0.25` `SUT <1.0 at n>=0.25` unless gated `frontierHitRate==1.0` | not run |
| `P-STAGEHAND-TTL` (PRIMARY SUT) | correlated `probeHit ~1.0 at n0 ~0.5 at n0.25 accuracy>=0.90 saving>=30%` `per_hit <=0.85 vs RAG at n0/n0.25 <=1.20 vs StagehandCache` `UNKNOWN>=0.85 ECE<=0.15 rho_proxy_real>=0.50 n_non304>=800` | not run — correlated `10+30ms HEAD If-None-Match ETag W/body_sha` not exercised |
| `P-WEBMCP-TOOL` | `714/2147 O(1) 15+10ms lookup 800/f compile` `M_total Pareto 897 vs 3703` `rho_proxy_real>=0.50 supersede` | not run — registry not built |
| `P-SPIDER-MEA-BATCHED` (contrast) | `per_hit 1.12>0.85 vs RAG fail reproduced unless TN 0.986` via shared WAL | not run |

`control_verdict=FAIL` — correctly reflects `PC` precedence gate; `NC`/`B`/`P` as `unknown` is honest missing-data per `EXPERIMENT_PACKET.md` §1, not hidden falsification.

---

## 6. Metrics — All Null Is Honest Missing Data

`result.json:metrics.diagnostics` — `true` for docker daemon reachable, `false` for all distributed subcomponents (shared WAL, PyJWT, gunicorn), `binary-only-1.24.0-no-upstream` for nginx, `false` for numpy/scipy/sklearn/pandas/browsergym/playwright/gpt key, `null` for `n_non304`/`health_gated`, `false` for `rho_proxy_real_computable`/`bootstrap5000_computable`, `d926279d` for kernel patch, `3/3 PASS` for unittest, `frozen_inputs_mutated false`.

`result.json:metrics.primary` — 40+ entries all `null`: `per_hit_ratio_STAGEHANDTTL_vs_RAG_n0`/`n0_25`, `per_hit_ratio_WEBMCP_vs_RAG_* f=10/f=100`, `per_hit_ratio_STAGEHANDTTL_vs_STAGEHANDCACHE/TERX/SPIDER`, `rho_proxy_real`, `rho_novelty_per_hit_STAGEHANDTTL/WEBMCP`, `rho_total`, `rho_length_*` pooled+per-stratum, `rho_shuffled`, `fresh_at_n0_rate`/`stale_at_n0_25_rate`/`probe_accuracy`/`probe_saving`/`probe_correlated_vs_random_delta`/`probeFalseAccept`, `false_accept`/`UNKNOWN_precision`/`ECE_exec`/`ECE_bootstrap_upper`/`confidence_std`, `success_n0`/`mean_success`, `M_total_f10_*` tokens `M_per_hit_f10_*` `M_total_f100_*`, `distributed_TN`/`per_node_TN`/`n_non304_measured`, `toolHitRate`/`frontierHitRate`/`cacheHitRate`/`webmcp_registry_size`, `Pareto_dominance_*`, `per_hit_vs_M_total_supersede_flag`. All explicitly `null` with `metric_units_notes` stating thresholds for `SURVIVES` (see `result.json`).

**No `n*3200` bijective cost, no seeded-42 random staleness proxy, no fabricated Pareto.** This is the correct handling of `MEASUREMENT_INVALID` per packet (missing-data vs negative-result). Ancestor economics ceiling remains bounded to **file-proxy only** (`192/36 orthogonal alias families 630 pairs `Jaccard 0.0` `QCR TAU0.30` `f=10` seeded-42 stale: `StagehandTTL per_hit 1.045 CI[1.034,1.056]>0.85 at n0` fails `<=0.85 at both n0 and n0.25`; WebMCP `1.032>0.85` at `n0` and `0.88>0.85` at `f=100`; `rho 0.472<0.60` `|rho_length| 0.306>0.20`; Pareto `M_total_f10 WebMCP 897 vs Stagehand 1773 vs RAG 3703 vs Cold 5497` tokens `latency 1799 vs 7265` hidden `per_hit` artifact where both hit same `50-tok` verify path excludes `retrieval 200+150ms vs tool_lookup 15+10ms vs probe 10+30ms`).

---

## 7. Validity Notes, Unresolved & Carry-Forward

**Validity Notes (7, verbatim in `result.json:validity_notes`):**

1. Infrastructure failure is not scientific negative — carries parent bounded falsification ceiling only.
2. Frozen prohibition on file-proxy fallback honored — `RAW EVIDENCE -> OBSERVATION -> DERIVED` preserved.
3. Correlated freshness gap unmeasured — `probe_is_correlated` never set.
4. Proxy fidelity gap unmeasured — supersede undecidable without `rho_proxy_real>=0.50` + `n_non304>=800`.
5. Kernel fix scope disclosure — only `src/spider/kernel.py` 1 insertion within allowed roots, no constitutional edits.
6. Degenerate CI guard disclosure — would have flagged `[1,1]` but no CI produced.
7. Next retry requirements — `rho_proxy_real`/`rho_length`/`rho_shuffled`/`n_non304>=800` health-gated + `bootstrap 5000` all required before claim.

**Unresolved (6, in `result.json:unresolved`):** Whether distributed `TN 0.986` flips `per_hit` + `rho` gates; whether correlated `ETag W/body_sha fresh~1.0 vs 50% stale` achieves `saving>=30% accuracy>=0.90`; whether `M_total_f10 Pareto` should supersede `per_hit` per Director second clause; whether `f=100` flips WebMCP `0.88>0.85`; whether runtime will land fixture; whether `C-PRODUCT-ECON` remains `REJECTED` bounded on file-proxy or moves to `EXPERIMENTAL`.

**Inherited `carry_forward` (preserved `USE`, mandate binding):**

- *Established (durable):* Kernel dot-regex patch `d926279d` `3/3` PASS; frozen inputs byte-identical; `MEASUREMENT_INVALID` gate correctly enforced (not `FALSIFIED`); maximum justified ceiling is parent bounded falsification on file-proxy (`1.045`, `1.032`, `0.472`, `0.306`, `897 vs 3703` artifact); `RAW EVIDENCE -> OBSERVATION` separation preserved.
- *Rejected (bounded to 192/36 file-proxy honest `f=10`):* StagehandTTL+TTL seeded-42 `~50%` stale `REJECTED` at `1.045>0.85`; WebMCP `714/2147 15 tok` `REJECTED` at `1.032>0.85` / `0.88>0.85 f=100`; `per_hit ~1.0 at n0` is metric artifact.
- *Unknown (what this PIVOT tests):* Whether distributed `TN 0.986` + `BrowserGym 2000-node full-DOM` + `rho_proxy_real>=0.50` flips parity and `|rho_length|<0.20`; whether correlated `fresh~1.0 vs 50% stale correlated` achieves saving/accuracy gates; whether `M_total Pareto` supersedes `per_hit`; whether `f=100 L 8-14 widening` flips; whether runtime hardening lands.
- *Do_not_assume (preserved verbatim 10 items):* `MEASUREMENT_INVALID` ≠ `FALSIFIED`; `per_hit ~1.0` ≠ viability (excludes retrieval/tool/probe); seeded-42 `0.53` ≠ correlated CDN `fresh~1.0`; bounded to `192/36 L 8-14 f=10` not global; `M_total Pareto` co-primary not secondary; per-node `TN 0.667` prohibited; `docker_available false` prior `rho_proxy_real` unmeasured; `f=100 0.88>0.85` exploratory secondary; kernel fix required; `control_verdict FAIL` ≠ audit fail; `M_total` without `rho`/`n_non304` not claimable; `single-worker sticky $request_uri` required.

---

## 8. Product Consequence

**None beyond preserving correct gate.** This `MEASUREMENT_INVALID` (`INCONCLUSIVE`) transaction **does not** move `C-PRODUCT-ECON` from `HYPOTHESIS`/`REJECTED` bounded on file-proxy to `EXPERIMENTAL`, does not support `SURVIVES_CURRENT_TEST`, `SUPERSEDE`, `FALSIFIED`, or `MIXED`. It correctly reaffirms the Director `PIVOT` comparative reasoning: *continuing per_hit sweep with same batched-MEA file-proxy is exploitation with no decision change;* the decisive gate requires **distributed correlated health-gated substrate + `rho_proxy_real>=0.50` + Pareto**.

Consequences per frozen `spec.json`:

- If future valid run achieves `SURVIVES_PRIMARY` (`C1`+`C2`+`C3`+`C4`+`C5` PASS with `PC1-PC5` PASS including `TN>=0.85` `n_non304>=800` `BrowserGym 2000-node rho_proxy_real>=0.50` correlated probe `fresh~1.0 stale~0.5 accuracy>=0.90 saving>=30%` calibration valid) → `C-PRODUCT-ECON` `HYPOTHESIS→EXPERIMENTAL` bounded to `WebArena-Verified v2 192/36` orthogonal distributed file+Docker single-worker sticky, and `C-FRESHNESS` `HYPOTHESIS→EXPERIMENTAL` for correlated `TTL/ETag` probe with `TN 0.986` health-gated.
- If `SUPERSEDE` (`C1+C2+C5 PASS` but `C3 per_hit >0.85` and `C4 Pareto` dominates decisively with `rho_proxy_real>=0.50` per-stratum `|rho_length|<0.20 n_non304>=800 correlated delta>10%`) → formally supersede `per_hit=(M_total - retrieval - compile - auditor)/L <=0.85` with `M_total_f10 Pareto` as primary O(1) gate before any `PRODUCT_CORE` promotion (metric-design change per Director second clause).
- If `FALSIFIED_PRIMARY` (`controls PASS` but `per_hit>0.85` via honest distributed frozen formula with correlated probe health-gated, or Pareto not dominant or `rho_proxy_real<0.50` or `n_non304<800`) → **PARK residual-novelty/WebMCP economics permanently on distributed correlated substrate** (not just file-proxy) and pivot product to `ST-WebAgentBench CuP` or Intel product-page sampling before any `PRODUCT_CORE`.

Current transaction satisfies **none** of these and remains `BLOCKED pending runtime hardening`.

---

## 9. Reproduction & Provenance

**Reproduce audit:**

```bash
PYTHONPATH=src python3 -m unittest tests.test_kernel -v  # 3/3 PASS, kernel d926279d
cat research/experiments/EXP-PRODUCT-35936223443/artifacts/substrate_audit.json  # OBS-1..OBS-19
cat research/experiments/EXP-PRODUCT-35936223443/result.json | python3 -m json.tool | head -n 120
cat research/experiments/EXP-PRODUCT-35936223443/failure.json
cat research/experiments/EXP-PRODUCT-35936223443/provenance.json
```

**Determinism:** Audit is deterministic; kernel patch is deterministic; no model calls/network/browser calls performed due to block (expected `<2 min`). Re-running without runtime hardening will reproduce same `MEASUREMENT_INVALID`.

**Provenance (see `provenance.json`):** `base_sha c2b97ca2`, `pre_execute bedd6205`, `post_execute 8dccde1c` (uncommitted kernel patch only), frozen hashes `a3532d5d`/`b4403f1b`/`c64f2b23`/`6e75efa3` parent handoff `EXP-PRODUCT-35932494797 8766d9cb`, code changes 1 insertion, environment Python `3.12.14` Linux `6.17.0-1022-azure` docker daemon reachable but image absent, no key.

**Smallest Next Action (from `failure.json`):**

> `runtime: deploy distributed HS256 shared-WAL substrate at /tmp/spider-runtime/shared.db (or /tmp/spider-runtime-35936223443/shared.db) WAL mode, per-batch SELECT honest sum counters, HS256 PyJWT 2.14.0 shared-secret, 1x gunicorn 23.0.0 single-worker + nginx 1.24.0 $request_uri sticky hash, health-gated URL-sticky real If-None-Match/ETag W/body_sha 200 vs 304 validated 960/960 oracle-free TN>=0.85 vs per-node 0.667 artifact, n_non304>=800; provision Docker BrowserGym 0.14.3 CDP AX 2000-node 1280x720 Playwright 1.63.0 + gpt-4o-mini API key for 15-step tokens/browser+latency (rho_proxy_real>=0.50, per-stratum |rho_shuffled|<0.20 |rho_length|<0.20); install scientific stack numpy+scipy+sklearn+pandas for family-stratified bootstrap 5000 / trajectory-grouped block-permutation 5000 and TFIDF Jaccard TAU0.30 ranker; keep kernel dot-regex patch sha d926279d.`

Until that lands, any product `per_hit` or `M_total` Pareto claim remains `HYPOTHESIS` bounded to `192/36 file-proxy` (`REJECTED`), and no `PRODUCT_CORE` promotion is authorized.
