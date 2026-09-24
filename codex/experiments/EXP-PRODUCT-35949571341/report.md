# EXP-PRODUCT-35949571341 — Product Pareto supersession gate (health-gated single-worker sticky)

**Lane:** product — `src/spider/kernel.py` + `tests/` + `sdk/` (allowed roots `src, tests, sdk, pyproject.toml`)
**Claims:** `C-PRODUCT-ECON` (primary) — subsidiary `C-RESIDUAL-NOVELTY`, `C-FRESHNESS` evaluated as secondary
**ID:** `EXP-PRODUCT-35949571341` — cycle `35949179364` — Director mandate `CONTINUE` with `cognitive_reset true`
**Status:** `MEASUREMENT_INVALID` — `INCONCLUSIVE` — no economics measured — substrate absent as in parent `EXP-PRODUCT-35947481519`
**Frozen inputs:** `request.json` `bd1734ba` `spec.json` `42b085fa` `prereg.md` `cced2e99` byte-identical to `freeze.json` — not mutated

---

## 1. What was asked (Director binding question)

> On health-gated shared-WAL HS256 substrate (single-worker sticky `$request_uri` hash, `If-None-Match/ETag->304 n_non304>=800` probe, TTL 60s max-age conditional probe with ETag W/body_sha ~50% stale at n=0.25 vs ~1.0 at n=0) plus Docker BrowserGym 0.14.3 2000-node 1280x720 real gpt-4o-mini 15-step tokens/browser_steps+latency with `rho_proxy_real>=0.50` and per-stratum `|rho_shuffled|<0.20` and `|rho_length|<0.20`, does honest `M_total_f10 Pareto` dominance (tokens vs browser+latency vs accuracy at `f=10/100`, 5000 family-stratified bootstrap + 5000 block-permutation) superseding contested `per_hit=(M_total_f10 - retrieval - distill/compile - auditor)/L <=0.85` show Stagehand selector-cache+TTL vs WebMCP Registry 714 sites/2147 tools O(1) compilation (amortized 800/f) vs SGDR/AWM state-grounded retrieval achieving dominance vs `RAG-EMBED TAU0.30 QCR` with verification-derived calibration `false_accept<=0.10 UNKNOWN>=0.85 ECE<=0.15 bootstrap upper<=0.18` ...

This is the **smallest high-information test that can change `PRODUCT_CORE` decision** per `prereg.md:1`: if `per_hit<=0.85` survives on distributed correlated substrate it reopens `C-PRODUCT-ECON` to `EXPERIMENTAL`; if `per_hit` still fails but `M_total_f10 Pareto` dominates decisively it formally supersedes `per_hit` as the viability gate (metric-design change); if both fail it PARKs residual-novelty/WebMCP/SGDR economics permanently on distributed correlated substrate and pivots to CuP/diverse-site grounding.

All thresholds are family-stratified pooled `N~192` on **distributed HS256 shared-WAL health-gated URL-sticky `$request_uri` `n_non304>=800` single-worker sticky + Docker BrowserGym 2000-node 1280x720** with honest summed branch counters (no `n*3200`), correlated TTL gating (`fresh_at_n0 ~1.0` vs `~50%` stale at `n0.25` `n_non304>=800`), SGDR state_key index, real `gpt-4o-mini` tokens, and `rho_proxy_real>=0.50`.

## 2. Raw substrate audit — the entire transaction is blocked

EXECUTE ran the exact substrate diagnostics mandated by `spec.json:measurement_validity` and `prereg.md:4` **before any outcome-bearing measurement**. All are `NOT TESTABLE`:

| Dependency | Required by frozen design | Observed |
|---|---|---|
| Shared SQLite WAL | `/tmp/spider-runtime/shared.db` WAL mode per-batch SELECT HS256 PyJWT 2.14.0 | `ls /tmp/spider-runtime` → `No such file`; `find /tmp -name shared.db` → no hit (permission-denied systemd dirs only); `shared_wal_db_exists false` |
| HS256 auth | PyJWT 2.14.0 HS256 shared-secret | `python3 -c "import jwt"` → `ModuleNotFoundError: No module named 'jwt'` |
| gunicorn | 1x gunicorn 23.0.0 single-worker sticky | `which gunicorn` → not found; `import gunicorn` → ModuleNotFoundError |
| nginx sticky | nginx 1.24.0 `$request_uri` sticky hash health-gated | binary 1.24.0 present but `nginx -T` → stock config, no `upstream`/`proxy_pass`/`$request_uri` hash, `[emerg] open() /run/nginx.pid failed (13: Permission denied)` — not configured |
| Scientific stack | numpy/scipy/sklearn/pandas for bootstrap 5000 + block-perm 5000 | all four `ModuleNotFoundError` — bootstrap/permutation uncomputable |
| BrowserGym | BrowserGym 0.14.3 CDP AX 2000-node 1280x720 Playwright 1.63.0 | `import browsergym` / `playwright` → ModuleNotFoundError; `docker images` → only 6 gh-aw images, no BrowserGym image; `docker_browsergym_configured false` |
| Real tokens | gpt-4o-mini 15-step `rho_proxy_real>=0.50` | `OPENAI_API_KEY` absent (empty env); `rho_proxy_real` unmeasurable |
| Fixtures | 192/36 orthogonal WebArena census, QCR TAU0.30 bank, WebMCP 714/2147, SGDR 36 state_key | `/tmp/webarena` absent; `fixtures/` absent; `research/harness` absent |
| Kernel binding | `_PARAMETER` dot-regex `r"\$\{[A-Za-z_][A-Za-z0-9_\.]*\}"` patch d926279d, 5/5 EXECUTABLE confidence>=0.80 | HEAD is `r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}"` without dot — `sha 46929b3a` — secondary PC2 gap |
| Conditional probe | `HEAD If-None-Match/ETag W/body_sha` correlated `n_non304>=800` health-gated | `n_non304 null`; probe not exercised; `If-None-Match` not exercised |

Per `spec.json:falsifier` and `prereg.md:5` precedence: **any** `PC failure or degenerate CI [1,1] or artifact or `n_non304<800` or `If-None-Match` not exercised or health-gate failed or `rho_proxy_real` unmeasurable or SGDR index missing or kernel dot-regex not patched → `MEASUREMENT_INVALID` **irrespective of economics** with no file-proxy fallback. All five primary gates fire by absence; the transaction was **not completed**.

No `~2628` deterministic `resolve/_bind/probe/registryLookup/SGDR rerank/MockEnv` trials were run on a substitute isolated SQLite. No `n*3200` bijective proxy and no seeded-42 random staleness fallback were fabricated. This honors `prereg.md:4` and `AGENTS.md` failure discipline: *infrastructure failure is not a scientific negative*.

## 3. Controls (frozen identities preserved)

All controls retain their frozen identifiers. All are `UNKNOWN` (not testable) rather than `PASS/FAIL` because the distributed pipeline health-gated `$request_uri` single-worker sticky on which they must be exercised does not exist.

- **Positive** `PC-DISTRIBUTED-PARETO-CORRELATED-SINGLE` (`PC1-PC5`): exact-repeat `hitRate 1.0 ~50 tok` via shared WAL `TN>=0.85` health-gated `n_non304>=800`; orthogonal `Jaccard<0.30` max `0.0` + kernel binding `1.0/1.0 confidence>=0.80` + correlated probe `fresh ~1.0 at n0 stale ~0.5 at n0.25 accuracy>=0.90 saving>=30%` + registry `714/2147 1.0 at n0 15 tok` + SGDR `36 hitRate>=0.5 180 tok`; non-vacuous `false_accept 0.10-0.60`; frozen-formula within `1e-6` via honest distributed sum counters `rho_proxy_real>=0.50`; distributed WAL `960/960 TN>=0.85` + BrowserGym `rho_proxy_real>=0.50`. **Observed:** `UNKNOWN` — all paths require absent substrate.
- **Null** `NC-DISTRIBUTED-SHUFFLE-PIPELINE-SINGLE` (`NC1-NC4`): trajectory-grouped permutation of `parameter_slots` + TTL valid_key to seeded-42 random `0.53` decorrelated + WebMCP/SGDR key swaps + `|rho_shuffled|<0.20 p>=0.20`; random cache; length-constant `L*500 rho~0 R2~0`; ablations `TTL correlated vs random delta >10%`, `WebMCP vs SGDR <20%`, `shared TN 0.986 vs per-node 0.667`. **Observed:** `UNKNOWN` — requires same distributed pipeline + numpy/scipy for permutation 5000.
- **Baselines** `B-COLD`, `B-RAG-EMBED`, `B-STAGEHAND-CACHE`, `B-TERX-REPLAY`, `B-BROWSERBASE-MCP` and **SUTs** `P-STAGEHAND-TTL` (primary), `P-WEBMCP-TOOL`, `P-SGDR-AWM`, `P-SPIDER-MEA-BATCHED`: all `UNKNOWN` — each requires the same shared WAL health-gated substrate + fixture census.

See `result.json:controls` for per-control `expected_behavior`, `observed_behavior`, and `evidence_refs` pointing to the exact substrate audit lines above.

## 4. Metrics

`result.json:metrics` is `{}` — checked and empty — because the measurement transaction could not complete validly. No proxy `per_hit` (e.g. file-proxy `1.045>0.85` / `1.032>0.85`), no Pareto `M_total_f10` (e.g. `897 vs 3703`), no `rho_proxy_real`, `rho_novelty`, `rho_length`, `rho_shuffled`, `ECE`, `UNKNOWN_precision`, `false_accept`, `n_non304`, or safety violation rates are reported here. Reporting file-proxy numbers would violate the frozen prohibition on substituting isolated SQLite for the distributed WAL substrate and would collapse `RAW EVIDENCE -> INTERPRETATION` (see `validity_notes`).

The `5000` family-stratified bootstrap and `5000` block-permutation CIs/p-values are also `{}`, because `numpy/scipy/sklearn/pandas` are absent even for offline computation.

## 5. Interpretation (bounded, not exceeding evidence)

- **Not a falsification.** Per `research/EXPERIMENT_PACKET.md:1` mandatory-key semantics, `status=MEASUREMENT_INVALID` + `outcome=INCONCLUSIVE` is not `FALSIFIES`. The contested `per_hit=(M_total_f10 - retrieval/tool_lookup/SGDR - distill/compile - auditor)/L <=0.85` (falsified `1.005>0.85 rho 0.363<0.60` on honest file-proxy, and `1.045>0.85` on `192/36` bounded file-proxy at `f=10`) is **neither confirmed nor rescued** by this transaction. The artifact warning (`per_hit` excludes `retrieval 200 vs tool 15 vs SGDR 180 vs probe 10` where both hit same `50-tok` verify path, making ratio `~1.0` by construction) remains a hypothesis awaiting a valid run.

- **Not a supersession decision.** The Director's second clause — *does `M_total_f10 Pareto` dominance with `rho_proxy_real>=0.50` supersede `per_hit` as `PRODUCT_CORE` gate?* — is **entirely undecided**. The supersede condition (`per_hit>0.85` but Pareto saving `>=30%` Stagehand `>=50%` WebMCP `>=25%` SGDR, `accuracy>=0.85`, `rho_proxy_real>=0.50`, `|rho_length|<0.20`, `n_non304>=800` single-worker sticky, correlated probe delta `>10%` vs random, safety non-inferior) cannot be evaluated without a valid measurement.

- **Maximum justified ceiling unchanged.** The only bounded economics that remains justified is the parent file-proxy ceiling inherited from `EXP-PRODUCT-35947481519` / `EXP-PRODUCT-35916130502`: `192/36` orthogonal alias families `630` pairs `Jaccard 0.0` `QCR TAU0.30` at honest `f=10` `StagehandTTL 1.045 CI[1.034,1.056]>0.85` `WebMCP 1.032>0.85` `rho 0.472 |rho_length| 0.306` `Pareto WebMCP 897 vs Stagehand 1773 vs RAG 3703 vs Cold 5497`. This transaction does not expand, narrow, or promote that ceiling.

- **Product consequence:** none. `C-PRODUCT-ECON` remains `HYPOTHESIS` (registry `3511a788`) bounded `REJECTED` on file-proxy only. No promotion to `EXPERIMENTAL` or `PRODUCT_CORE` is warranted from a measurement-invalid cycle. The `C-FRESHNESS` correlated-TTL guard (`fresh at n0 ~1.0 via ETag 200 vs ~50% stale at n0.25 via 304`) and SGDR state-conditioned retrieval (`180 tok` vs `200` RAG vs `15` WebMCP) remain `HYPOTHESIS`/`unknown` on the distributed substrate.

## 6. Validity, representation loss, and threats

- **Decision-rule compliance:** The transaction correctly followed the frozen precedence `PC failure > health-gate > economics` and did not invent a file-proxy result. This is the correct handling of a runtime dependency failure per `spec.json:decision_rule` (`Docker replication does gate SURVIVES — if distributed single-worker sticky substrate or rho_proxy_real unavailable or n_non304<800 ... -> MEASUREMENT_INVALID not FALSIFIED`).

- **Kernel dot-regex threat:** The current `HEAD` missing dot is a secondary PC2 threat. Even after the runtime hardening, the binding spot-check must be re-verified (5/5 per-family `n0` `EXECUTABLE` with correct `bound_action` via `kernel.resolve`). The tree was deliberately kept clean this cycle because the primary gate already fails; provenance logs the gap as `46929b3a`.

- **No proxy validity leakage:** No `n*3200`, no seeded-42 random staleness `0.53` used as SUT, no per-node `TN 0.667` artifact, no `within-family std==0` degeneracy were reported. All such nulls remain `UNKNOWN`.

- **Ceiling effects:** If later provisioned, BrowserGym full-DOM `2000-node 1280x720` hash truncation (`non-hash-truncated AX up to 5k`) and SGDR `state_key` hash collisions must be disclosed as representation loss. ST-WebAgentBench safety `CuP` taxonomy was not measured; it is correctly reported as `unresolved null` not `PASS`.

## 7. What remains unresolved (for the next pulse)

See `result.json:unresolved` (11 items). The **smallest next action that could unblock** this gate is:

> **runtime hardening:** provision health-gated shared SQLite WAL HS256 HS256 PyJWT 2.14.0 `1x gunicorn 23.0.0 single-worker + nginx 1.24.0 $request_uri sticky hash` with `If-None-Match/ETag->304 n_non304>=800` fixture at `/tmp/spider-runtime/shared.db` (WAL mode per-batch SELECT) + `pip install numpy/scipy/scikit-learn/pandas` for bootstrap/permutation + BrowserGym 0.14.3 2000-node 1280x720 `Playwright 1.63.0` Docker image + `gpt-4o-mini` key for `rho_proxy_real` + WebArena `192/36` orthogonal fixtures (`qcr_bank_manifest`, `webmcp_registry 714/2147`, `sgdr_index 36`) + re-apply kernel dot-regex patch `d926279d`; then re-run the frozen `192`-task census with honest distributed sum counters (no `n*3200`, no file-proxy fallback) and report both `per_hit` and `M_total_f10 Pareto` with `5000` bootstrap + `5000` block-permutation and safety CuP.

Until then, repeating the same file-proxy `per_hit` sweep is negative expected value per Director `comparative_reasoning` — the economics question cannot move without the distributed correlated substrate.

---

*Evidence refs:* `research/experiments/EXP-PRODUCT-35949571341/result.json` (controls `PC-DISTRIBUTED-PARETO-CORRELATED-SINGLE`, `NC-DISTRIBUTED-SHUFFLE-PIPELINE-SINGLE` with `evidence_refs`), `provenance.json` (`environment` block with `shared_wal_db_exists false`, `health_gated false`, `n_non304 null`, `jwt_present false`, `docker_browsergym_configured false`), frozen `spec.json`/`prereg.md`/`freeze.json` hashes `42b085fa`/`cced2e99`/`bd1734ba` verified byte-identical.

