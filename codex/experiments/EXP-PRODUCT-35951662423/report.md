# EXP-PRODUCT-35951662423 — EXECUTE report (product lane, C-PRODUCT-ECON)

Status: **MEASUREMENT_INVALID** — outcome **INCONCLUSIVE**. This is an infrastructure/substrate
failure per the frozen falsifier precedence (1), not a scientific negative. The frozen claim
(C-PRODUCT-ECON Pareto supersession on health-gated single-node HS256 + BrowserGym) remains
untested; no economics number in this report should be read as evidence about the claim.

## What was executed

1. **Frozen-input verification.** Re-hashed all frozen inputs; byte-identical to `freeze.json`
   (prereg `49c6027f…`, request `a4dfe539…`, spec `4225441b…`). Also confirmed working-tree HEAD
   `5930a02a` with pre-existing dirty entries (`M codex/index.json`, untracked
   `model_execute.json`) untouched.

2. **MV2 kernel dot-regex patch (in-scope product code change, required by frozen MV2).**
   `src/spider/kernel.py` line 12 `_PARAMETER` patched from
   `r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}"` to the frozen form
   `r"\$\{([A-Za-z_][A-Za-z0-9_\.]*)\}"`. Post-patch sha256
   `d926279d5ee14a044a2f13b8abc09202df9f5adb9e86feaadeb61818a15f4038` — the first 8 hex chars
   `d926279d` exactly match the frozen prereg's referenced patched-sha prefix, i.e. this is the
   patch content the design anticipated.

   Verified on the real kernel (no substrate needed for this gate):
   `PYTHONPATH=src python3 -m unittest tests/test_kernel.py` → 3/3 PASS (no regression);
   MV2 spot-check (frozen-style mechanisms with `family+intent+site` preconditions,
   dot-nested slots `${item.id}/${family.id}/${site.name}`, confidence 0.85) →
   **5/5 EXECUTABLE with correct dot-nested binding**; unknown family abstains UNKNOWN;
   confidence-0.5 mechanism returns EXPLORE, not EXECUTABLE. Raw results:
   `artifacts/mv2_kernel_spot_check.json` (5/5 PASS).

3. **Environment/substrate audit (raw evidence).** `artifacts/env_audit.json` records:
   Python 3.12.14 / pip 26.2.1 with **working PyPI network**; scientific stack now installable
   (numpy 2.5.3, scipy 1.18.1, sklearn 1.9.1, pandas 3.0.6, flask 3.1.3, pyjwt 2.15.0,
   gunicorn 26.2.0, requests 2.34.2 — all import OK; the parent had this as absent); Docker
   28.0.4 present but only 6 gh-aw firewall images; `docker pull` **denied** for both
   `ghcr.io/servicenow/browsergym:0.14.3` and `browserless/browsergym`; `OPENAI_API_KEY` **unset**
   (no other model keys); `/tmp/spider-runtime` and `/tmp/spider-runtime/shared.db` **absent**;
   nginx 1.24.0 binary present (no sticky/health-gated config); `sgdr_index` **not found**
   anywhere in `research/` (maxdepth 4); frozen-bank prior-run artifacts verified in-repo
   (qcr_bank_manifest 36 families TAU0.30, webmcp_registry 2147 lines/714 site_id — matches the
   frozen 714/2147 identity, cost_config).

## Falsifier precedence resolved (frozen rule, not my judgment)

Precedence (1) fires on **multiple independent DIE triggers**:

| Trigger (frozen) | Evidence this cycle | Status |
|---|---|---|
| single-node HS256 not provisioned at /tmp/spider-runtime/shared.db single-worker sticky | dir/db absent; nginx present but unconfigured | FIRED |
| Docker BrowserGym 0.14.3 + gpt-4o-mini key unavailable (rho_proxy_real unmeasurable) | image pulls denied; no OPENAI_API_KEY | FIRED |
| n_non304 < 800 | n_non304 null (no probe substrate) | FIRED |
| SGDR index 36 state_key missing | not found repo-wide | FIRED |
| kernel dot-regex not patched | **now patched + verified 5/5** | **CLEARED this cycle** |
| TRAIN contamination | not assessable (no census ran) | N/A |

Per the frozen rule ("irrespective of economics, no file-proxy fallback, no n*3200 bijective
proxy"), no economics metrics were computed, proxied or inferred. All economics metric keys are
`null` (explicitly unknown, per packet contract — not zero, not negative results).

## Controls

Preserved frozen identifiers: `PC-SINGLE-NODE-PARETO-CORRELATED`, `NC-SINGLE-NODE-SHUFFLE-PIPELINE`,
and baselines `B-COLD`, `B-RAG-EMBED-TAU030-QCR`, `B-STAGEHAND-CACHE`, `P-STAGEHAND-TTL`,
`P-WEBMCP-TOOL`, `P-SGDR-AWM`. Details in `result.json`. Summary:

- PC2 kernel sub-gate: **PASS** (5/5 EXECUTABLE, confidence>=0.80, dot binding, guards).
- All other PC1–PC5 / NC1–NC4 / baseline gates: **UNKNOWN** (require the absent substrate);
  PC5 is effectively FAIL (substrate not provisioned, n_non304 null) — which is itself one of the
  frozen MEASUREMENT_INVALID triggers, recorded as infrastructure failure.

## Smallest next actions (from `unresolved` in result.json)

1. Provision `OPENAI_API_KEY` (gpt-4o-mini) + a pullable BrowserGym 0.14.3 Docker image
   (2000-node 1280x720 CDP AX) → then rho_proxy_real pooled+per-stratum becomes measurable.
2. Provision the single-node substrate exactly per MV3: `/tmp/spider-runtime/shared.db` SQLite WAL,
   single-worker gunicorn, nginx `$request_uri` sticky, PyJWT HS256, real If-None-Match/ETag 304
   loop, n_non304>=800; reconcile gunicorn 26.2.0 vs frozen 23.0.0 and PyJWT 2.15.0 vs 2.14.0.
3. Build `sgdr_index.json` (36 state_key, TRAIN-only) and stage the frozen fixture set for this
   experiment (192/36 census, qcr_bank_manifest, webmcp_registry 714/2147, cost_config).
4. Then run PC1–PC5 + NC1–NC4 on the actual pipeline, then C1–C4 with bootstrap5000/permutation5000
   before any SURVIVES/FALSIFIED/SUPERSEDE verdict.

## Interpretation vs evidence discipline

- RAW EVIDENCE: `artifacts/env_audit.json`, `artifacts/mv2_kernel_spot_check.json`, hashes above.
- OBSERVATION: substrate/key/fixture absences as listed; kernel patch applied and passing.
- DERIVED MEASUREMENT: MV2 5/5 EXECUTABLE at confidence>=0.80; 3/3 unit tests; frozen hashes match.
- INTERPRETATION: transaction is MEASUREMENT_INVALID by frozen precedence (1); this does **not**
  falsify C-PRODUCT-ECON; file-proxy numbers from prior runs remain bounded file-proxy evidence
  only (do_not_assume).