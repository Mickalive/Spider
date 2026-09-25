# EXP-PRODUCT-36089498872 — Execution Report (Product lane)

## Claim under test

`C-LLM-INHERIT` (frozen): SPIDER's parameter inheritance (kernel binds `family.attr` dot-paths to previously visited family values) produces a single-family LLM-inherit gap `>= 0.12` vs strong baselines (`B-COLD`, `B-INSTRUCTIONS`, `B-RAG-EMBED-TAU030-QCR-K5`, `B-STAGEHAND-CACHE`) on a contamination-free rebuilt holdout (`101e481d`, `0/36` disjoint, Jaccard `0.0`, qcr `8c69804b`), health-gated single-node substrate plus Docker BrowserGym, with calibration/verification `>=25%` saving and `rho_proxy >= 0.50` per stratum.

## Verdict

- **status** (result.json): `MEASUREMENT_INVALID`
- **outcome**: `INCONCLUSIVE`
- **Reason**: Frozen decision rule — BrowserGym absent (GHCR pull `denied`), `OPENAI_API_KEY` absent, kernel durability gate not committable by EXECUTE. No claim update. The bounded diagnostics below are valid measurements, not claim inference.

## What was measured (all valid, RAW evidence in artifacts/)

| Gate / control | Result | Evidence |
|---|---|---|
| MV1 rebuilt holdout | **PASS** — sha `101e481d…` staged; local deterministic rebuild `fa70b5b2…` byte-content-identical except `experiment_id` metadata; 0/36 pool+usage contaminated families; cross-family max Jaccard 0.0; qcr bank `8c69804b…`; L ∈ {8..14} constant within family; novelty 36/39/39/39/39 | `fixture_checks.json` |
| MV3 kernel dot-regex | **FUNCTIONAL PASS, durability pending** — kernel working-tree sha `d926279d…` == frozen; 5/5 dotted slots EXECUTABLE; wrong-family → UNKNOWN; commit not made (workflow forbids) | `mv3_kernel_spot_check.json` |
| MV4 single-node freshness | **PASS** — 400 non-304 (200/200 stratified), If-None-Match exercised 100%, errors 0, WAL single worker, HS256-only; TN 1.0 sticky & direct | `substrate_probe.json` |
| MV5 correlated TTL/ETag | **PASS** — n0 hit 1.0, n0.25 accuracy 1.0, false_accept 0.0, saving 0.40, delta 0.4067 vs random 0.5933 | `substrate_probe.json` |
| MV6 BrowserGym + LLM | **BLOCKED (MEASUREMENT_INVALID)** — ghcr pull denied, docker login non-TTY denied, OPENAI absent; Playwright 1.63.0 `accessibility()` API removed; no `rho_proxy_real` | `browser_health.json`, `attempts_log.json` |
| PC1 exact-repeat | **PASS (file-proxy half)** — 5/5 hit, 50 tok/hit; BrowserGym half blocked | `pc1_exact_repeat.json` |
| PC3 verification calibration | **PASS** — AUROC 0.8714 vs shuffled 0.4681; precision 0.9491; forced-EXEC wrong-accept 0.1607 ∈ [0.10,0.60]; conf_std 0.4543; UNKNOWN precision 0.9837; ECE 0.107, 0 empty bins | `pc3_verify_calibration.json` |
| PC4 frozen-formula parity | **PASS (proxy arithmetic)** — 192 rows, max abs diff 5.7e-14; `rho_proxy_real` NULL (blocked) | `null_controls.json` |
| NC1 shuffled | **FAIL (partial)** — band pass (−0.1367) but p = 0.0724 and rho_length −0.2871 > 0.10; deterministic file-proxy coupling disclosed | `null_controls.json` |
| NC1b/NC1c/NC2/NC3/NC4 | PASS — nonexistent-family UNKNOWN 1.0; shuff-exec AUROC 0.463; keys AUROC 0.462 UNKNOWN 0.654; length-const rho 0.008; ablation delta 0.4067 TN 1.0 | `null_controls.json` |
| Economics (bounded ceiling) | SPIDER 1981.09 vs COLD 5992.71 (−66.9% saving, CI [0.652,0.687]); vs RAG ratio **1.5064** (CI [1.4796,1.5306]) — **breaches frozen ceiling 0.85**; vs INSTRUCTIONS 0.3247; vs STAGEHAND 0.4198; browser+latency saving 0.494; resolve proxy 1.0/1.0/0.7656/0.7656 | `economics.json`, `economics_per_trajectory.csv` |

## Interpretation

- The substrate and controlled-fixture half of the design is **fully operational and reproducible**: after fixing a stale-process infrastructure artifact (leftover gunicorn/nginx from two earlier crashed runs served probes against a deleted DB → 500s), a single clean provision yields n=400 stratified, TN 1.0, correlated delta 0.41, zero errors.
- The **bounded honest-counter economics** reproduce the parent's arithmetic exactly (0.669 saving; per-hit 74.3 @ novelty 0.0 / 161.5 @ 0.25) and show the SUT's token ratio vs RAG on the parameter-cutoff proxy **exceeds** the frozen 0.85 ceiling. Per frozen decision rule and precedent this is a **diagnostic, not falsification**: the claim test requires real BrowserGym trajectories and gpt-4o-mini tokens, both unavailable.
- Verification/calibration machinery (PC3) passes its frozen gate, so the verify/repair half of the mechanism remains a candidate, but AUROC on MockEnv does **not** transfer to gpt-4o-mini (frozen `do_not_assume`).
- NC1's rho_length failure is a deterministic-coupling artifact of file-proxy counters (same-family length confounding), already anticipated in the frozen disclosure; fixing it requires real trajectories.

## Required fixes to unblock a claim test (also in `validity_notes` / `unresolved`)

1. Grant GHCR pull of `ghcr.io/servicenow/browsergym:0.14.3` (or mirror image) and export `OPENAI_API_KEY`; then run step 9 (browser) of `run_experiment.py`.
2. Authorize a kernel commit so MV3 durability can be re-hashed (`d926279d…` is the expected post-patch working-tree sha; HEAD is `8af66ccf…`).
3. Decide whether to vendor `webarena_verified` (Hard258 188-family census was not staged).
4. Redesign NC1 against real trajectories to break same-family length confounding.

## Reproducibility

`run_experiment.py` (sha `e0c7f3e8…`) reproduces all artifacts end-to-end in ~10 s:
`/opt/hostedtoolcache/Python/3.12.14/x64/bin/python3 research/experiments/EXP-PRODUCT-36089498872/run_experiment.py`