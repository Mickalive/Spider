# EXP-PRODUCT-35777355953 — Product-kernel port of Frontier RECONSTRUCTION-RULE

- **Experiment id**: EXP-PRODUCT-35777355953
- **Lane**: product
- **Claim**: C-SEMANTIC-RESOLVE (product-kernel instantiation)
- **Status / outcome**: `COMPLETE` / `SUPPORTS` (bounded to synthetic orthogonal+mixed; live exploratory)
- **Frozen inputs**: `request.json`, `spec.json`, `prereg.md`, `freeze.json` (hashes in `freeze.json`) — unmodified

## Question

Does porting the audit-PASS Frontier RECONSTRUCTION-RULE into the product kernel
(`SpiderKernel.resolve(reconstruct=True)` in `src/spider/kernel.py`), conditioned only on
observation-derived state (url/header/body/AX), resolve semantic aliasing on the frozen
synthetic strata — 30 orthogonal + 10 mixed multi-channel — without false accepts,
miscalibration or regression vs the reference proxy?

## Method (frozen design)

- **Fixtures**: 70 synthetic tasks mechanically identical in composition to the audit-PASS
  Frontier harness: 40 alias-OOD (families 0–2: header `ApiKey`/`X-Reset-Token`/`Authorization Bearer`,
  body `apiKey`/`key`/`api_token`/`token`, auth `scope`/`admin_scope`/`permission`/`X-Scope`
  novel forms held out; family 3: mixed header+body+query in one request), 12 exact-match,
  12 no-applicable, 6 empty-registry. Leak check 0/40. All `derived_context` keys ⊆
  `ALLOWED_STATE_KEYS`; no forbidden keys present.
- **Methods (8)**: `P-SPIDER-RECONSTRUCT` (product port through the public kernel API),
  `R-FRONTIER-RULE-PROXY` (verbatim reference adapter snapshot `frontier_proxy.py`, sha-anchored to
  the audit-referenced Frontier harness `4db542a727…`), `B-EXACT-MATCH`, `B-VERBATIM-REPLAY`,
  `B-RAG-TFIDF`, `B-RAG-EMBED` (unavailable, disclosed), `B-RANDOM`, `B-INSTRUCTION`
  (unavailable, disclosed).
- **Port**: pure-stdlib transcription of `choose_adoptions` + `rewrite_template_multi`
  (adopt-any-observed-key-not-in-registry, alphabetically sorted), structural scoring
  (slot count / path-segment Jaccard+prefix / query / header / body channels), softmax over
  candidates at temperature 0.15 + deterministic jitter, confidence-gated `UNKNOWN` at <0.80,
  reads only `ALLOWED_STATE_KEYS`. Identical arithmetic to the numpy reference
  (max-subtraction softmax, first-tie argmax), no new product dependencies.
- **Statistics**: Wilson 95% CI, one-sided binomial vs 0.10, paired McNemar (with continuity
  correction), 5-bin ECE, 2000-resample block bootstrap ECE CI, seeds 42/43/44 registry-order
  stability splits.
- **Economics**: wall-clock latency per method; 0 LLM tokens / 0 browser calls for all
  deterministic methods; B-INSTRUCTION requires an LLM agent (unavailable).

## Results

| Metric (id in `result.json` / `derived_metrics.json`) | Value | Gate |
|---|---|---|
| `P-SPIDER-RECONSTRUCT::alias-OOD::correct_rate` | **1.0 (40/40)**, Wilson [0.912, 1.0] | C3 ≥0.50 ✔ |
| `P-SPIDER-RECONSTRUCT::alias-OOD::false_accept_rate` | **0.0** | C4 ≤0.15 ✔ |
| `P-SPIDER-RECONSTRUCT::orthogonal_subset::correct_rate` | **1.0 (30/30)** | C3 ✔ |
| `P-SPIDER-RECONSTRUCT::mixed_subset::correct_rate` | **1.0 (10/10)**, FA 0.0 | C3 mixed ≥0.40 ✔ |
| `P-SPIDER-RECONSTRUCT::heldout_9::correct_rate` | **1.0 (9/9)** | C3 ✔ |
| `P-SPIDER-RECONSTRUCT::per_family` | fam0 1.0, fam1 1.0, fam2 1.0, fam3 1.0 | C3 ✔ |
| `R-FRONTIER-RULE-PROXY::alias-OOD::correct_rate` | **1.0 (40/40)** (parity anchor) | C8 ✔ |
| Baselines on alias-OOD | exact 0.0, verbatim FA **1.0**, tfidf 0.0, random 0.0 | C4 gap 1.0 ✔ |
| `P-SPIDER-RECONSTRUCT::ECE_all_strata` | **0.0653**; proxy 0.0803; |C8 delta| = 0.015 ≤0.05 ✔ (C6 ≤0.15 ✔) |
| `P-SPIDER-RECONSTRUCT::confidence_std` | 0.400 (not constant; bins 1–3 empty, disclosed) | C6 ✔ |
| `${P}::no-applicable::unknown_precision` / `false_accept_rate` | **1.0 / 0.0** (12/12 UNKNOWN) | C2/C6 ✔ |
| `${P}::empty-registry::unknown_rate` | **1.0** (6/6) | C2 ✔ |
| `${P}::exact-match::correct_rate` | **1.0 (12/12)**; proxy 1.0; baseline 1.0 | C1/C5 ✔ |
| `stats::binomial_p_vs_0.10` | **1.00e-40** | C3 ✔ |
| `stats::mcnemar_correct_vs_exact` / `mcnemar_fa_vs_verbatim` | **6.98e-10 / 6.98e-10** | C3/C4 ✔ |
| `C8::per_family_max_gap` | **0.0** | C8 ≤0.10 ✔ |
| `stability::cv_3_seeds` | **0.0** (1.0/1.0/1.0 across seeds 42/43/44) | reported |
| Harness errors / template leak / forbidden-key reads | **0 / 0 / 0** | audit ✔ |

**Decision rule**: gates C1–C8 all pass → `status=COMPLETE`, `outcome=SUPPORTS`
(claim SURVIVES bounded to synthetic orthogonal+mixed with live exploratory).

## Interpretation

- The port is behaviorally identical to the reference proxy on the frozen synthetic design:
  40/40 pooled, per-family gap 0, ECE within 0.015. No integration regression in the
  `SpiderKernel.resolve(reconstruct=True)` boundary (whitelist projection, candidate
  filtering, `_bind`).
- The discrimination story is structural, not retrieval: verbatim replay false-accepts 40/40
  and TF-IDF retrieval resolves 0/40, while the reconstruction adapter abstains (UNKNOWN) on
  all 12 no-applicable and 6 empty-registry controls with precision 1.0.
- Mixed multi-channel tasks (header `X-Api-Key` + body `api_token` + query `permission`
  simultaneously aliased against single-channel training mechanisms) resolve 10/10, showing
  compositional `adopt-any-observed-key-not-in-registry` rewriting rather than fixture
  memorization (leak 0/40, held-out 9/9).
- Per the frozen consequence mapping, this advances C-SEMANTIC-RESOLVE to
  "VALIDATED at product-kernel level bounded to genuine reconstruction on tested orthogonal
  families plus mixed composition with calibrated UNKNOWN" — PRODUCT_CORE candidate pending
  replication on live BrowserGym, learned GRPO/System-One stability, end-to-end economics at
  scale, and audit PASS.

## Controls

- **PC-EXACT-MATCH**: PASS — product 12/12, proxy 12/12, baseline 12/12, FA 0.
- **PC-BROWSERGYM-HEALTH**: FAIL (0/0 attempted) — `browsergym.webshop` and
  `browsergym.alfworld` modules are absent from the browsergym 0.14.3 distribution on this
  runner (exact `ModuleNotFoundError`s in `browser_probe.json`). Per the frozen C1 clause this
  correctly **bounds live to exploratory** (not MEASUREMENT_INVALID). Chromium + CDP AX
  substrate verified separately at 1280x720 (example.com: 15 AX nodes).
- **NC-NO-APPLICABLE**: PASS — UNKNOWN precision 1.0, FA 0.0.
- **NC-EMPTY-REGISTRY**: PASS — 6/6 (100%) UNKNOWN.

## Validity notes (selected; full list in `result.json`)

1. Live WebShop/ALFWorld stratum unmeasured (module absence, substrate verified). Claim is
   bounded to synthetic orthogonal+mixed.
2. B-RAG-EMBED and B-INSTRUCTION unavailable per frozen sanctions → TFIDF is the strong
   retrieval baseline in C7; no fabricated metrics.
3. Empty-registry abstention confidence differs product (0.0 default) vs proxy
   (0.05–0.068 intent-hash score) — both abstain; drives the disclosed 0.015 ECE delta.
4. Stability CV = 0.0 because reconstruction scoring is order-invariant; the 3 registry
   splits are deterministic per-task permutations of identical content (noted in artifacts).
5. Kernel port present in working tree (sha `a5726515…` vs pre-port `46929b3a…`); EXECUTE
   scope rules forbid committing — `git diff HEAD` is available for AUDIT.

## Economics (report; non-gating)

- `P-SPIDER-RECONSTRUCT`: mean 0.436 ms/task (70 tasks; retrieval+reconstruction+bind),
  0 LLM tokens, 0 browser calls; amortized latency per successful alias-OOD task 0.436 ms.
- All deterministic methods: 0 tokens/calls. B-INSTRUCTION (200 tokens amortized f=10)
  unmeasured — requires an LLM agent (no provider key).

## Reproduction

```
python3 research/experiments/EXP-PRODUCT-35777355953/run_experiment.py   # from repo root
python3 -m pytest tests/ -q                                              # kernel tests (10 passed)
```

Deps (installed in-runner): numpy, scipy, scikit-learn, pytest, playwright 1.44.0
(+chromium), browsergym 0.14.3.