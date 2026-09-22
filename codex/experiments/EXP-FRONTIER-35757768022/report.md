# EXP-FRONTIER-35757768022 — Genuine state-conditioned reconstruction for orthogonal header/body/auth aliasing

**Lane:** frontier · **Claim:** C-SEMANTIC-RESOLVE · **Status:** `COMPLETE` · **Outcome:** `SUPPORTS` (SURVIVES_CURRENT_TEST, bounded)

## 1. Context

The Director mandate (`request.json:director_mandate`) reopened C-SEMANTIC-RESOLVE to test whether a genuine
(non-oracle) state-conditioned reconstruction adapter generalizes beyond the parent synthetic URL-only POC
(EXP-FRONTIER-35752577234, 30/30 rule-based, ECE 0.0738) to **orthogonal alias families** — header-based
(ApiKey/X-Reset-Token/Authorization), body JSON field (apiKey/key/token), and auth permission (scope/admin_scope/
X-Permission) — as the confirmatory synthetic stratum, with live BrowserGym WebShop/ALFWorld and a learned
GRPO/System-One variant as additional arms when the substrate exists.

Frozen decision rule (spec.json / prereg.md): `SURVIVES_CURRENT_TEST` iff PC + NC pass, S1–S5 hold, and the
reconstruction is not dominated by retrieval; `MEASUREMENT_INVALID` if PC/NC fail, an oracle leak is detected
(forbidden-key access or test-template-in-registry), confidence is constant, or alias-OOD N < 24.

## 2. Design executed (frozen, unchanged)

- **60 synthetic tasks:** 30 alias-OOD (3 families × 10: 7 standard prefix/resource combos + 3 held-out novel
  forms) + 12 exact-match + 12 no-applicable + 6 empty-registry.
- **Registry per alias-OOD task:** exactly one training mechanism (documented form, conf 0.9) + one distractor
  alias form (conf 0.9) + one low-confidence distractor (conf 0.8); **all three share the test intent
  deliberately** (exact-matcher failure must come from template aliasing, not intent mismatch).
- **Leak-free by construction:** the expected/test template is a form **not present in its registry**
  (standard-7 test = documented DOC[2] form across 7 prefix/resource bases; held-out-3 tests = novel forms
  X-Api-Key/X-Auth-Key/Api-Token, api_token/authToken/access_key, permission/access_scope/X-Scope).
  `assert leak == 0` passes; re-verified on serialized `tasks.json`: **0/30**.
- **Genuine non-oracle adapter:** `reconstruct_resolve(intent, derived_context, retrieved_candidates, params)`
  reads only whitelisted observation fields (`ALLOWED_STATE_KEYS`: url/method/url_path/url_query/url_segments/
  headers_observed/body_observed/ax_*). `derive_state()` asserts 0 forbidden-key violations. Confidence is
  derived from structural scores (softmax temp 0.15 + deterministic jitter, gate <0.80 → UNKNOWN); no hardcoded
  constant. Selection branch when a candidate structurally matches observed state; adoption-rewrite branch
  otherwise (transcribes observed channel key and re-slots the value, keeping documented template structure).
- **Methods:** B-EXACT-MATCH, B-VERBATIM-REPLAY, B-RAG-TFIDF, B-RAG-EMBED (unavailable → disclosed, TFIDF is
  the strong retrieval baseline), B-RANDOM, RECONSTRUCTION-RULE, RECONSTRUCTION-LEARNED (unavailable → disclosed).

## 3. Results (all stable identifiers as in `derived_metrics.json`)

| Stratum / metric | RECONSTRUCTION-RULE | Baselines |
|---|---|---|
| alias-OOD correct_resolution | **30/30 = 1.0** Wilson [0.886, 1.0] | exact 0/30, verbatim 0/30 (FA 30/30), TFIDF 0/30, random 0/30 |
| alias-OOD false_accept | **0.0** Wilson [0.0, 0.114] | verbatim 1.0 (gap = 1.0 ≥ 0.15) |
| per family (10 each) | fam0 10/10 · fam1 10/10 · fam2 10/10 | — |
| held-out-9 (novel forms) | **9/9 = 1.0**, FA 0.0 | — |
| exact-match (PC) | 12/12 = 1.0 | B-EXACT-MATCH 12/12 = 1.0 |
| no-applicable (NC) | UNKNOWN precision **1.0**, FA **0.0** | all evaluated methods 1.0 / 0.0 |
| empty-registry (NC) | UNKNOWN 1.0 | all evaluated methods 1.0 |
| ECE (5 bins, all strata) | **0.0758**; bootstrap 2000 mean 0.0759 CI [0.0666, 0.0850] | — |
| confidence std | 0.395 (varies, not constant) | — |

Statistics: one-sided binomial p = 1.0e-30 vs 0.10 null · McNemar vs B-EXACT-MATCH (correct) p = 1.19e-07
(b=30, c=0) · McNemar FA vs B-VERBATIM-REPLAY p = 1.19e-07 (b=0, c=30). Harness errors: 0 (510 raw rows).

**Decision gates:** PC ✔ · NC-NO-APPLICABLE ✔ · NC-EMPTY ✔ · S1 ✔ (≥0.50 + binomial + McNemar) · S2 ✔
(FA ≤0.15, ≥0.15 below verbatim, McNemar) · S3 ✔ (exact ≥0.90) · S4 ✔ (precision ≥0.85, ECE ≤0.15) · S5 ✔
(not dominated by retrieval: best RAG 0.0 vs reconstruction 1.0). `controls_pass=True`, `all_survives=True`.

### Channel-isolation diagnostics (exploratory, non-gated)

- RULE-URL-ONLY: 0/30 — with only the URL channel the adapter abstains (no credential signal), i.e., no
  hallucinated reconstruction on ambiguous state.
- RULE-BODY-ONLY: 10/30 — correct exactly on fam1 (body family) only.
- RULE-HEADERS-ONLY: 20/30 — correct exactly on fam0+fam2 (header families) only.

The family↔channel mapping matches the fixture design exactly, confirming the adapter's correct behavior comes
from the observed credential channel (as intended for an observation-derived, non-oracle mechanism), not from
leaked fixture signals.

## 4. Interpretation (bounded, per frozen decision rule)

SUPPORTS = SURVIVES_CURRENT_TEST **bounded to the synthetic orthogonal families (header/body/auth), including
the held-out novel forms**, for this genuine rule-based reconstruction adapter. Live BrowserGym (WebShop/
ALFWorld) and the learned GRPO/System-One arm were **not measurable** in this environment (no browsergym/
playwright/offline-LLM modules) and are disclosed rather than fabricated; per the frozen spec they do not
trigger MEASUREMENT_INVALID — they bound the claim ceiling. Product consequence from the frozen rationale:
a reconstruction layer after retrieval (critique-reconstruct conditioned on intent + observation-derived state,
confidence-gated UNKNOWN < 0.80) is supported for these alias families; PRODUCT_CORE remains unauthorized until
learned-adapter stability and live-browser replication (plus end-to-end economics) replicate at scale.
C-SEMANTIC-RESOLVE ceiling: bounded EXPERIMENTAL (rule-based, orthogonal synthetic); claim-status updates are
the Director's verdict, not asserted here.

## 5. Validity threats (see `result.json:validity_notes` and `unresolved`)

- Synthetic-to-real gap: minimal derived dict (no real DOM/AX), so drift to production SPAs/session/auth is
  unproven.
- Bimodal confidence distribution (18 abstain ~0.05, 42 accept ~0.92–0.98) dominates 5-bin ECE; calibration
  under other conventions remains a caveat (parent carry-forward).
- Intent deliberately equal across registry+test on alias-OOD; baseline 0/30 does not imply retriever failure
  on intent-dissimilar corpora.
- All methods deterministic with SEED=42; TFIDF corpus = per-task registry (train only).

## 6. Files

- `result.json`, `derived_metrics.json`, `raw_evidence.json`, `tasks.json` in
  `research/experiments/EXP-FRONTIER-35757768022/`
- Harness: `research/frontier/run_genuine_35757768022.py` (code root per `research/lanes/registry.json`)
- `provenance.json` for hashes, environment, and reproduction commands.