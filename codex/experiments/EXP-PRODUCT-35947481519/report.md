# EXP-PRODUCT-35947481519 — Execute Report (product)

**Experiment:** EXP-PRODUCT-35947481519 · **Lane:** product · **Status:** `MEASUREMENT_INVALID` · **Outcome:** `INCONCLUSIVE`
**Claims:** `C-PRODUCT-ECON` (primary, Director PIVOT binding) + subsidiary `C-RESIDUAL-NOVELTY`, `C-FRESHNESS` (secondary, unmeasured).
**Frozen inputs:** verified byte-identical to `freeze.json` (`request.json` `afb09f5a`, `spec.json` `51095b6b`, `prereg.md` `3749be58`; registry sha `3511a788` matches request). Git HEAD `272767ff`, tree clean (only machine `model_execute.json` untracked). No frozen file was mutated; `src/` was deliberately left unmodified.

---

## 1. What was asked (frozen Director PIVOT)

On a health-gated HS256 shared-WAL single-worker sticky substrate (`$request_uri` hash, real If-None-Match/ETag→304, `n_non304>=800`) with correlated TTL-60s freshness (fresh at n=0 ~1.0 vs ~50% stale at n=0.25), Docker BrowserGym 0.14.3 2000-node full-DOM real gpt-4o-mini 15-step cost (`rho_proxy_real>=0.50`, per-stratum `|rho_shuffled|<0.20`, `|rho_length|<0.20`), do Stagehand selector-cache+TTL gating vs WebMCP Registry 714/2147 O(1) compilation (800/f amortized) vs SGDR/AWM state-grounded retrieval achieve honest `M_total_f10` Pareto dominance with verification-derived calibration (`false_accept<=0.10`, `UNKNOWN>=0.85`, `ECE<=0.15`, bootstrap upper `<=0.18`), thereby superseding contested `per_hit<=0.85` as the PRODUCT_CORE gate, with ST-WebAgentBench safety gating?

## 2. What was done (exact frozen design, no redesign)

EXECUTE ran the substrate-gating audit first, per frozen falsifier precedence (PC failure / `n_non304<800` / If-None-Match not exercised / sticky violated / `rho_proxy_real` unmeasurable → `MEASUREMENT_INVALID` irrespective of economics; file-proxy fallback prohibited):

1. Checked both canonical shared-WAL paths (`/tmp/spider-runtime/shared.db`, `/tmp/spider-runtime-35947481519/shared.db`) plus a `/tmp`-wide search — **no `shared.db` anywhere accessible**.
2. Checked auth/serving stack — **PyJWT absent, gunicorn absent**; nginx 1.24.0 binary present but stock config (no upstream, no `$request_uri` sticky) and daemon not startable here.
3. Checked statistics stack — **numpy/scipy/sklearn/pandas all absent** → bootstrap 5000 / block-permutation 5000 uncomputable.
4. Checked real-token replication — **browsergym and playwright absent**; Docker 28.0.4 present but **no BrowserGym image**; **no gpt-4o-mini/OPENAI key** → `rho_proxy_real` unmeasurable.
5. Checked census fixtures — `/tmp/webarena` and repo `fixtures/` both absent; no `tasks.json`, QCR bank, `714/2147` registry, `36` SGDR index, or `cost_config`.
6. Checked binding fix — `src/spider/kernel.py:12` still `r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}"` (no dot; patch `d926279d` not applied) — secondary PC2 gate also unmet.
7. **Stopped before any outcome-bearing measurement.** No 192-task census, no per_hit/Pareto/calibration/safety numbers were run or fabricated on any substitute substrate.

## 3. Results

There are no economics results to report. `result.json` carries `status=MEASUREMENT_INVALID`, `outcome=INCONCLUSIVE`, `metrics={}`, all 11 control/baseline entries (`PC-DISTRIBUTED-PARETO-CORRELATED-SINGLE`, `NC-DISTRIBUTED-SHUFFLE-PIPELINE-SINGLE`, `B-COLD`, `B-RAG-EMBED`, `B-STAGEHAND-CACHE`, `B-TERX-REPLAY`, `B-BROWSERBASE-MCP`, `P-STAGEHAND-TTL`, `P-WEBMCP-TOOL`, `P-SGDR-AWM`, `P-SPIDER-MEA-BATCHED`) as `pass_fail=UNKNOWN` with `observed_behavior=NOT TESTABLE`, 11 raw observations, 8 validity notes, 10 unresolved items. `provenance.json` records the full environment audit; `failure.json` records the substrate failure with the smallest next action. Raw evidence (absence listings, import errors, hashes) is preserved in `result.json:observations` and `provenance.json:environment`, kept distinct from the interpretation below.

## 4. Interpretation (bounded, no claim update)

This is **infrastructure failure, not a scientific negative**. It neither supports nor falsifies `C-PRODUCT-ECON`, `C-RESIDUAL-NOVELTY`, or `C-FRESHNESS`, and it does not expand, contract, or supersede any prior ceiling. The maximum justified economics ceiling remains the inherited parent bounded falsification on file-proxy only (StagehandTTL `1.045 CI[1.034,1.056]>0.85` at n0; WebMCP `1.032>0.85`; `rho 0.472`; `|rho_length| 0.306`; Pareto WebMCP `897` vs RAG `3703` vs Cold `5497` — a reporting pattern, not a gated viability claim). The Director's second-clause supersession question (Pareto replacing `per_hit<=0.85` as PRODUCT_CORE gate) is **entirely undecided** pending a valid measurement with `rho_proxy_real>=0.50`, per-stratum `|rho_length|<0.20`, `n_non304>=800`, correlated probe delta `>10%` vs random, SGDR-vs-WebMCP delta reported, and safety non-inferiority. Safety is reported as null (unmeasured), not PASS. `UNKNOWN` is the valid product answer for this transaction.

## 5. Validity notes and representation loss

- Docker-engine presence and nginx-binary presence are explicitly **not** counted as substrate availability (no image, no upstream, no sticky config, no keys, no WAL).
- The kernel dot-regex gap would fail PC2 independently, but the primary gate is substrate absence alone; `src/` was left untouched to keep the tree clean since patching could not change the outcome.
- `pytest` is not installed here, so even the existing `tests/test_kernel.py` suite could not be executed in this environment; its hash is recorded for the auditor.
- No proxy economics, no `n*3200` sums, no seeded-42 staleness numbers are reported — the frozen prohibition on file-proxy substitution was honored.

## 6. Smallest next action (no new child experiment authorized here)

Retry this **identical frozen transaction** only after runtime hardening lands (in priority order): (1) shared SQLite WAL at `/tmp/spider-runtime/shared.db` (WAL mode, per-batch SELECT, HS256 PyJWT 2.14.0, 1× gunicorn 23.0.0 single-worker + nginx 1.24.0 `$request_uri` sticky, health-gated If-None-Match/ETag 200-vs-304, `n_non304>=800`, `960/960` oracle-free `TN>=0.85`); (2) Docker BrowserGym 0.14.3 CDP AX 2000-node 1280x720 + Playwright 1.63.0 + gpt-4o-mini key; (3) numpy/scipy/sklearn/pandas for bootstrap/block-permutation 5000; (4) kernel dot-regex patch `d926279d` with 5/5 n0 EXECUTABLE verification; (5) TRAIN-only fixtures (192/36 orthogonal QCR bank TAU0.30, WebMCP 714/2147 registry, SGDR 36 state_key index, cost_config). If the substrate is still unavailable, keep PARK per the parent handoff and pivot product effort to ST-WebAgentBench CuP or Intel diverse-site grounding per the Director's comparative reasoning — a decision for the Global Research Director and lane DIRECTOR, not this EXECUTE stage.
