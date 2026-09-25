# EXP-PRODUCT-36091881382 — EXECUTE report (product lane, claim C-LLM-INHERIT)

- **Experiment:** EXP-PRODUCT-36091881382 (REOPEN of EXP-PRODUCT-36089498872, Director mandate `action=REOPEN`, `parent_handoff_disposition=USE`, `cognitive_reset=true`)
- **Claim:** C-LLM-INHERIT — LLM-inheritance economics with freshness-gated Jaccard 0.85 + deterministic repair + correct-family dot-regex reconstruction vs B-COLD / B-INSTRUCTIONS / B-RAG-EMBED-TAU030-QCR-K5 / B-STAGEHAND-CACHE
- **Status:** `MEASUREMENT_INVALID` · **Outcome:** `INCONCLUSIVE`
- **Frozen inputs:** request.json `8ef87270…`, spec.json `afec9c54…`, prereg.md `1e67c0f9…` (all byte-identical to `freeze.json`)
- **Harness:** `run_experiment.py` `86a1b0e3…` (parent audited harness, packet identifiers only changed)

## 1. What was executed vs what was blocked

The run completed all 9 stages in 12.4 s. Two layers of result must be kept distinct:

| Layer | Machinery | Result |
|---|---|---|
| A. Instrument layer (deterministic, local) | fixture staging/checks, kernel spot-check, substrate probe, PC1 file-proxy half, PC3 MockEnv, honest-counter economics, null controls | Executed and measured (below) |
| B. Claim layer (browser + LLM) | MV6 Docker BrowserGym 0.14.3 2000-node CDP AX>10 1280x720, MV7 gpt-4o-mini 15-step per-trajectory tokens, C1–C5 decision gates | BLOCKED: GHCR pull `denied` (OBS-1), `OPENAI_API_KEY` absent (OBS-2) |

Per the frozen falsifier precedence (spec decision_rule / prereg §5), any of {PC failure, n_non304<360, BrowserGym absent, OPENAI absent, kernel not durable} ⇒ MEASUREMENT_INVALID irrespective of economics margins. Layer B's blockers each independently trigger this. **This is infrastructure/substrate failure, not scientific falsification** — the claim is neither supported nor falsified by this transaction.

## 2. Layer A results (measured)

### Fixtures (MV1/MV2) — PASS
- Staged holdout byte-identical to frozen artifact: sha `101e481d…` (192 tasks / 36 families, L 8–14 family-specific constant).
- `value_set_A ∩ B` empty on **all 36 families** (0 pool-level contaminated slots; 0 demo-vs-testB usage contaminated families).
- Cross-family bigram Jaccard over all **630 pairs: max 0.0** (nonzero pairs 0).
- qcr manifest sha `8c69804b…` tau 0.30; cost_config honors frozen 50/…/10.
- Hard258 census NOT staged (`webarena_verified` package absent) — frozen MV1 fallback to the rebuilt holdout applied.

### Kernel MV3 — functional PASS, durability FAIL
- Working-tree `_PARAMETER` regex is now the frozen dot form `r"\$\{([A-Za-z_][A-Za-z0-9_\.]*)\}"`.
- 5/5 dotted-slot resolve cases EXECUTABLE with exact bound URL; family gate UNKNOWN 5/5; unittest suite 4/4 (incl. new dotted-slots test).
- `mv3_durable_via_commit=false`: working tree sha `d926279d…` ≠ HEAD sha `8af66ccf…`; HEAD's kernel lacks dot support. EXECUTE is not authorized to commit, so the frozen durable-kernel gate is unmet (must be fixed by a code-owning step).

### Substrate MV4 (re-measured on this packet) — PASS
- `n_non304 = 400` (200/ep-a, 200/ep-b) ≥ 360 stratified; errors 0; If-None-Match fraction 1.0.
- Correlated freshness: n0 hit-rate 1.0; n0.25 accuracy 1.0, false-accept 0.0, TN_fresh 1.0; delta vs seeded Random(42) coin **0.407**.
- TN contrast sticky-vs-direct 1.0 / 1.0; WAL single-worker HS256; upstream set exactly `{127.0.0.1:18929}`; sticky log 1053 lines.
- Independent re-derivation from `probe_traces.jsonl` reproduces every number above.

### PC1 / PC3
- PC1 exact-repeat (file-proxy DOM-hash half): 5/5 hit-rate 1.0. BrowserGym AX half blocked.
- PC3 MockEnv calibration: AUROC true 0.871 vs shuffled 0.468; precision 0.949; forced-execute wrong-accept 0.161; confidence std 0.454; UNKNOWN precision 0.984; ECE 0.107 — all within frozen ranges; `pass=true`.

### Bounded-ceiling economics (honest counters, NOT claim economics)
- M_total_f10 tokens: B-COLD 5992.7 · B-INSTRUCTIONS 6101.7 · B-RAG-EMBED-TAU030-QCR-K5 1315.1 · B-STAGEHAND-CACHE 4719.3 · P-SPIDER-LLM-INHERIT 1981.1.
- Saving vs COLD f10: 0.669 (CI95 [0.652, 0.687]); browser-latency saving 0.494; SPIDER resolve-rate 1.0 vs RAG 0.234 / STAGEHAND 0.234 / COLD 0.0.
- SPIDER/RAG token ratio f10: 1.506 — SPIDER is **more expensive than RAG in this task-level counter model** (RAG's verbatim retrieval dominates at f10 on the rebuilt holdout). Directionally opposite of the frozen C4 saving claim: this is a diagnostic, gated by real-trajectory measurement.
- `rho_novelty_pooled 0.762` · `rho_length_pooled −0.287` (fails |·|<0.20).

### Null controls / PC4 (deterministic)
- NC1: rho_shuffled −0.137 (|·|<0.20 OK) but block-permutation p **0.072** (<0.20) and rho_length **−0.287** (|·|≥0.20) → `NC1_pass=false` (same coupling as parent).
- NC1b: nonexistent family UNKNOWN 1.0. NC1c shuffled AUROC 0.463 (expectation 0.45–0.60). NC2: UNKNOWN 0.654, AUROC 0.462 → pass. NC3: R2 4.3e-5 → pass. NC4 delta 0.407.
- PC4 frozen-formula parity: max abs diff 5.7e-14 ≤ 1e-6 → pass.

## 3. Interpretation

1. Instrument layer is **healthy and re-measured on this packet**: contamination-free holdout verified, single-node HS256 sticky substrate health-gated at n≥360 with TN 1.0 and non-zero correlated-vs-random gap, kernel dot-regex functional, calibration non-vacuous.
2. The claim-level transaction did **not** occur: no BrowserGym page, no real LLM tokens, no kernel durability commit. The frozen precedence therefore mandates `MEASUREMENT_INVALID` / `INCONCLUSIVE` — **not** FALSIFIES, despite the diagnostic SPIDER/RAG ratio 1.506 and NC1 fail, because both are measured at the bounded single-node ceiling where the frozen C1–C5 gates were never defined to run.
3. No file-proxy surrogation was used: all claim-level metrics are explicit `null`.

## 4. Validity threats & representation loss
- Single-node localhost latencies ≠ WAN; synthetic mutation driver ≠ real change distribution (VN-9).
- Deterministic counters encode per-step token structure, not calibrated model costs (VN-5).
- RAG retrieval modeled as 200 tokens + verbatim; real retrieval error rates unmeasured.
- rho_diagnostics per-family ~1.0 are honest-counter construction artifacts at the bounded ceiling, not claim evidence (VN-10).
- skate/maintenance risk: `sklearn`/`pandas` absent from pins (allowed by frozen gate list) (VN-8).

## 5. Unresolved & smallest next actions
1. **BrowserGym 0.14.3**: provide pullable image (GHCR credential/token with package read scope, or a mirror) — `docker pull ghcr.io/servicenow/browsergym:0.14.3` currently `denied`. Smallest next action: re-run with container registry read access.
2. **OPENAI_API_KEY**: provide a key so MV6 gpt-4o-mini 15-step trajectories and rho_proxy_real are measurable.
3. **Kernel durability**: commit the working-tree dot-regex kernel (sha d926279d) to HEAD via the authorized code-owning path; then `mv3_durable_via_commit=true`.
4. **Hard258 census**: install `webarena_verified` package to stage the Hard258/812 manifest (MV1 currently on frozen fallback holdout).
5. **NC1 coupling**: with real trajectories available, re-test rho_shuffled / per-stratum |rho_length| <0.20 and p≥0.20 to determine whether the deterministic −0.287 rho_length is a counter-model artifact or a real mechanism cost.
6. On all five fixes: execute the identical frozen design end-to-end; only a full BrowserGym+OPENAI run can produce a SURVIVES/FALSIFIES/MIXED verdict for C-LLM-INHERIT.

## 6. Evidence
All artifacts listed in `result.json::artifacts` with sha256; raw evidence preserved in `artifacts/probe_traces.jsonl`, `artifacts/env_audit.json`, `artifacts/substrate_start.json`, `artifacts/substrate_probe.json`, `artifacts/browser_health.json`, `artifacts/attempts_log.json`, plus `artifacts/*.json` derived metrics. Independent re-derivation script `/tmp/opencode/verify_exp.py` `32fbdc34…` confirms MV1/MV2/MV3/MV4/MV5 numbers and the f10 saving arithmetic.