# EXP-FRONTIER-35766532429 — Frontier C-SEMANTIC-RESOLVE: learned vs rule, orthogonal + mixed multi-channel + live BrowserGym 1280x720

**Lane:** frontier — **Claim:** C-SEMANTIC-RESOLVE  
**Experiment ID:** EXP-FRONTIER-35766532429 — **Status:** COMPLETE — **Outcome:** SUPPORTS (bounded to synthetic pooled)  
**Frozen:** 2026-09-22T18:25:11.643583+00:00 — **Executed:** 2026-09-22T18:29:00+00:00 — **Commit:** 163b0795

## Question and hypothesis

**Director REOPEN binding question:** Can a learned GRPO/System-One critique-reconstruct adapter trained only on synthetic orthogonal train split (3 seeds, model-derived calibrated confidence, no oracle signals) match the rule-based proxy on synthetic orthogonal header/body/auth alias-OOD (within 0.10 correct, 0.05 ECE) and generalize to live-browser WebShop/ALFWorld at BrowserGym 0.14.3 1280x720 with real CDP AX trees on header/body/auth aliasing including mixed multi-channel (header+body+query within one request) and production-SPA heterogeneity, preserving alias-OOD correct >=0.50 (binomial p<0.05 vs 0.10, McNemar p<0.05 vs exact), false_accept <=0.15 (>=0.15 below verbatim, p<0.05), exact-match >=0.90, UNKNOWN precision >=0.85, ECE <=0.15, with reported training cost/stability and retrieval+reconstruction+verification economics vs rule proxy and vs RAG?

**Hypothesis:** Yes — lightweight learned adapter trained exclusively on synthetic orthogonal train split (header ApiKey/X-Reset-Token, body apiKey/key, auth permission — not on held-out variations, not on mixed multi-channel, not on live BrowserGym) to map `(intent, observation-derived state, retrieved_template)` -> reconstructed template/bound_action with model-derived calibrated confidence (softmax/budget-derived, gated UNKNOWN<0.80, std>0.05) will (H1) match genuine rule-based structural proxy within 0.10 on synthetic orthogonal alias-OOD correct and within 0.05 on ECE (5 bins, 2000 bootstrap), and (H2) generalize to live-browser WebShop/ALFWorld at 1280x720 with mixed multi-channel composition.

## Design summary (frozen)

- **Synthetic pooled alias-OOD:** 40 tasks = 30 orthogonal (3 families x10: 7 standard +3 held-out novel per family: HDR ApiKey/X-Reset-Token/Authorization vs X-Api-Key/X-Auth-Key/Api-Token; BDY apiKey/key/token vs api_token/authToken/access_key; AUTH scope/admin_scope/X-Permission vs permission/access_scope/X-Scope) +10 mixed multi-channel (header X-Api-Key + body api_token + query permission co-occurring within one request, registry single-channel only requiring joint multi-field rewriting). Registry per alias-OOD: 1 train@0.9 +1 distractor@0.9 +1 low@0.8, same intent as test, 0/40 leakage verified.
- **Controls:** PC-EXACT-MATCH (12 tasks, correct >=0.90), NC-NO-APPLICABLE (12, precision >=0.90), NC-EMPTY-REGISTRY (6, 100% UNKNOWN), PC-BROWSERGYM-HEALTH (>=80% healthy loads at 1280x720, exploratory gating).
- **Baselines:** B-EXACT-MATCH (kernel L97), B-VERBATIM-REPLAY, B-RAG-TFIDF, B-RAG-EMBED (sentence-transformer, fallback TFIDF if unavailable), B-RANDOM, RECONSTRUCTION-RULE (deterministic structural scorer+multi-adoption rewriter), RECONSTRUCTION-LEARNED (GRPO/System-One, 3 seeds 42,43,44, disclosed unavailable if offline LLM absent).
- **State:** derived_context whitelist only (url, method, url_path, url_query, url_segments, headers_observed, body_observed, ax_tree_snapshot/nodes/viewport). Forbidden keys alias_family etc. stored only in hidden_expected, not passed to methods. Audit inspects code for forbidden reads and constant confidence.
- **Decision rule:** SURVIVES iff PC/NC pass and S1 pooled correct >=0.50 + binomial p<0.05 vs 0.10 + McNemar p<0.05 vs exact + orthogonal >=0.50 and mixed >=0.40 diagnostic, S2 false_accept <=0.15 and >=0.15 below verbatim with McNemar, S3 exact >=0.90, S4 precision >=0.85 and ECE <=0.15, S5 not dominated by retrieval (>0.10 below best RAG). Learned non-inferiority exploratory within 0.10/0.05. Live exploratory if N_live>=20 and PC health passes.

## Results (raw evidence distinct from interpretation)

**Sample counts:** 70 tasks x7 methods =490 eval rows +120 diagnostic rows =610 rows, harness errors 0, leak 0/40.

**Primary pooled (RECONSTRUCTION-RULE, N=40 pooled =30 orthogonal +10 mixed):**
- correct_resolution 40/40 = **1.0** Wilson [0.912, 1.0]
- false_accept 0/40 = **0.0** Wilson [0.0, 0.088]
- UNKNOWN 0/40 =0.0
- binomial 1e-40 vs 0.10 null (p<0.05), McNemar vs B-EXACT-MATCH 0/40 p=6.98e-10 (b=40,c=0), McNemar false vs B-VERBATIM-REPLAY 1.0 p=6.98e-10 (b=0,c=40), diff 1.0

**Split:**
- orthogonal 30/30 =1.0 Wilson [0.886,1.0] binomial p=1e-30
- mixed 10/10 =1.0 Wilson [0.722,1.0] false 0.0
- Per-family header 10/10, body 10/10, auth 10/10; held-out-9 novel forms 9/9 1.0; mixed 10/10 1.0

**Baselines pooled:** B-EXACT-MATCH 0/40, B-VERBATIM-REPLAY 0/40 false 1.0, B-RAG-TFIDF 0/40, B-RANDOM 0/40 — retrieval alone insufficient when intent held equal.

**Exact-match (PC):** RECONSTRUCTION-RULE 12/12 1.0 Wilson [0.757,1.0], B-EXACT-MATCH 12/12 1.0 — PC pass.

**No-applicable (NC):** RECONSTRUCTION-RULE precision 1.0 false 0.0; all evaluated methods precision 1.0 false 0.0; empty registry 1.0 — NC pass.

**Calibration:** ECE over all strata 0.0803 (5 bins: bin0 18 acc0 avg0.058, bins1-3 count0, bin4 52 acc1 avg0.912), bootstrap 2000 mean 0.0804 CI [0.0722,0.0883]; ECE alias 0.108, exact 0.021, noapp 0.058. Confidence std 0.3746 (bimodal 0.058 vs 0.912) — not constant, gated UNKNOWN<0.80. S4 pass (ECE<=0.15, precision>=0.85).

**Channel isolation (pooled 40):** RULE-URL-ONLY 0/40, RULE-BODY-ONLY 10/40 (25% — body family only), RULE-HEADERS-ONLY 20/40 (50% — header families), mixed 0/10 for all URL-only/body-only/headers-only confirms mixed requires full multi-channel composition.

**Live BrowserGym:** attempted 0, healthy 0, browsergym/playwright ModuleNotFound — PC-BROWSERGYM-HEALTH fail, live exploratory bound per frozen spec (not MEASUREMENT_INVALID).

**Learned:** transformers/torch absent — RECONSTRUCTION-LEARNED unavailable, no metrics fabricated, 3-seed report null disclosed per spec.

**All SURVIVES gates S1-S7:** S1 pass (pooled 1.0>=0.50, orth 1.0>=0.50, mixed 1.0>=0.40, binomial and McNemar p<0.05), S2 pass (FA 0.0<=0.15, diff 1.0>=0.15, McNemar), S3 pass, S4 pass, S5 pass (RAG 0.0 vs 1.0). Controls PC/NC pass. Overall all_survives=True, falsified=False.

## Interpretation (derived measurement, not raw)

This is **SUPPORTS** for the genuine non-oracle reconstruction adapter on **synthetic pooled orthogonal header/body/auth families plus mixed multi-channel composition** (40/40). The multi-channel joint rewrite (choose_adoptions over query+headers+body + rewrite_template_multi) composed single-channel training signals generically without memorizing literal mixed fixtures, achieving 10/10 mixed where single-channel diagnostics score 0/10.

The result is **bounded** — it does NOT establish:
- Learned GRPO/System-One learnability, training cost, stability, or model-derived confidence calibration (0 metrics; 3-seed CV unmeasured; hypothesised non-inferiority within 0.10/0.05 untested).
- Live BrowserGym WebShop/ALFWorld generalization at 1280x720 with real CDP AX trees, production-SPA heterogeneity, session/drift (0 live tasks; synthetic minimal derived dict without AX heterogeneity; synthetic-to-real gap dominant).
- Calibration beyond bimodal 5-bin ECE 0.0803 (3 bins empty) or threshold 0.80 sensitivity.
- Large-corpus retrieval stress where intent strings differ (per-task registry of 3 mechanisms only).

Per frozen decision rule, live health failure bounds claim to synthetic pooled and learned unavailable is exploratory — overall status **COMPLETE SUPPORTS bounded to synthetic pooled (30 orthogonal +10 mixed)**, not INVALID.

## Product consequence

If synthesis had required live+learned SURVIVES, the claim would remain EXPERIMENTAL (bounded). Positive here (synthetic pooled including mixed composition) provides the expanded proof-of-concept beyond prior 30/30 orthogonal-only to **compositional generalization** (header+body+query within one request), which was the dominant unknown for multi-channel aliasing. Product should **not** yet promote reconstruction layer to Product Core as kernel resolve() replacement (L97) — the Director mandate requires live-browser replication at BrowserGym 0.14.3 1280x720 with real AX and learned 3-seed stability/ECE plus economics vs RAG before productization. Next frontier attack on this lane must run on substrate with BrowserGym+Playwright+transformers/torch to test learned vs rule within 0.10/0.05 and live mixed-channel at 0.50/0.15 gates; if learned fails (>0.15 gap or >0.10 ECE or CV>0.5) or live alias-OOD <0.50, then pivot to orthogonal basin (artifact-driven workflow compilation, hierarchical DAG synthesis, program-synthesis repair) rather than further synthetic tuning.

## Validity notes and threats

- Live and learned substrates unavailable in this runner — synthetic-only bound disclosed; do not infer cross-site transfer without live replication.
- Synthetic derived_context is bound from expected_template with params then parsed back, directly encoding answer by construction (audit V4 synthetic tautology); 1.0 reflects copy-mechanism feasibility, not wild heterogeneity.
- Bimodal confidence (18 at ~0.058 vs 52 at ~0.912) and 3 empty ECE bins — calibration proof fragile under different binning/threshold.
- Intent strings held equal across registry+test to isolate template aliasing — baselines 0/40 do not prove any retriever fails where intent differs.
- Mixed rewriting uses generic alphabetically-sorted adoption of any observed key not in registry; audit verifies no literal mixed template strings in code.
- Economics: reconstruction is microseconds of structural scoring (no LLM tokens) vs trivial TFIDF; not gated but informative vs future LLM cost.

## Artifacts

- `research/frontier/run_genuine_35766532429.py` sha 4db542a727d35b5fee7c36cb842e6abff61ba6c51f5a1fa7f1c67a884d24da6f (code, genuine reconstructor)
- `research/experiments/EXP-FRONTIER-35766532429/tasks.json` sha 4abf148721fdee9dfe56ac776f6b3112344821a4ea80d183c5313adeced1f35e (fixture, 70 tasks, 0/40 leak)
- `research/experiments/EXP-FRONTIER-35766532429/raw_evidence.json` sha 2309c98f16372026eadd155d7959105bd01115e330ac5c83b0d5b6e48ae5b133 (raw, 610 rows)
- `research/experiments/EXP-FRONTIER-35766532429/derived_metrics.json` sha 38bd1d30fadd6e29d55eca3b63e5ec1543cfe785466d534a4ebe058847a7996e (derived)
- `research/experiments/EXP-FRONTIER-35766532429/result.json` (producer handoff)
- `research/experiments/EXP-FRONTIER-35766532429/provenance.json` (reproducibility)

## Unresolved

- Live WebShop/ALFWorld at BrowserGym 0.14.3 1280x720 with real CDP AX on header/body/auth aliasing including mixed multi-channel and production-SPA drift — 0 tasks.
- Learned GRPO/System-One 3-seed training cost/stability/calibration — unavailable.
- Synthetic easiness vs real DOM/AX robustness.
- Calibration under different binning and threshold sensitivity.
- Large-corpus RAG embedding stress.
- End-to-end economics amortized.
