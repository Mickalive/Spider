# EXP-FRONTIER-35773143736 Report

Lane: frontier · Claim: C-SEMANTIC-RESOLVE · Stage: EXECUTE · Schema v1

## 1. Executive Summary

The frozen sequenced test for **alias-out-of-distribution semantic resolution** was executed end-to-end on the synthetic task graph (70 tasks: 40 alias-OOD = 30 orthogonal + 10 mixed, 12 exact-match, 12 no-applicable, 6 empty-registry).

- A genuinely **learned** adapter — a compact MLP (46→128→64, ~15k params) trained with **GRPO** on 21 standard orthogonal tasks (leak-free: 0/9 held-out forms and 0/10 mixed templates in train) — reaches the same synthetic ceiling as the parent-validated rule proxy: **40/40 alias-OOD correct (30/30 orthogonal, 10/10 mixed), false-accept 0.0, held-out 9/9, mixed 10/10, across all 3 seeds (CV = 0.0)**.
- Its model-derived confidence (softmax over learned candidate scores + learned rewrite logit, learned temperature, gated UNKNOWN < 0.80) is **well-calibrated**: ECE 0.052, within the frozen 0.05 band of the rule's 0.080, with confidence std 0.39 ≫ 0.05 (no constant-confidence artifact).
- All frozen gates pass: **G0 (learned-vs-rule gap 0.0, ECE gap 0.028 ≤ 0.05, CV 0.0, pooled binomial p≈1e-40, McNemar p≈7e-10), rule S1–S7, learned S1–S5**, controls (PC-EXACT-MATCH, NC-NO-APPLICABLE, NC-EMPTY) and all five baselines behave as frozen (verbatim replay false-accepts 100%, retrieval baselines 0/40).

**Decision: STATUS COMPLETE, OUTCOME SUPPORTS** — SEQUENCED SURVIVES_CURRENT_TEST, bounded to the synthetic pooled evaluation. The live BrowserGym stratum is bound to exploratory and **could not be exercised** (browsergym.webshop/alfworld have no installable distributions, no playwright browsers; environment limitation disclosed — not a measurement failure, not a scientific negative). The learned arm is a compact GRPO adapter, **not LLM-scale GRPO**, per the frozen spec's allowance for a System-One scoring/budget adapter on a CPU-only runner.

## 2. Raw Evidence

All rows are direct per-task observations, written before any derived calculation (610 rows in `raw_evidence.json`; per-seed training/eval detail in `raw_evidence_learned_seeds.json`). `harness_errors = 0`.

| Statistic (observations) | Value |
|---|---|
| `fixture_identical_to_parent` | True (sha256 == parent tasks.json) |
| Train split n / heldout leak / mixed leak | 21 / 0 / 0 |
| Learned seeds & train wall s | 42: 8.67, 43: 8.6, 44: 8.5 |
| Final mean reward per seed | 1.241 / 1.240 / 1.218 (max 1.25) |
| RULE alias pooled correct / FA / UNKNOWN | 40/40 · 0.0 · 0.0 |
| LEARNED alias pooled correct / FA / UNKNOWN | 40/40 · 0.0 · 0.0 |
| RULE orthogonal / mixed | 30/30 · 10/10 |
| LEARNED orthogonal / mixed (FA) | 30/30 · 10/10 (FA 0.0) |
| Held-out 9 (rule / learned) | 9/9 · 9/9 |
| B-EXACT-MATCH / B-VERBATIM-REPLAY alias | 0/40 · 0/40 (FA 1.0) |
| B-RAG-TFIDF / B-RAG-EMBED / B-RANDOM alias | 0/40 · 0/40 · 0/40 |
| Channel isolation (URL-ONLY / BODY-ONLY / HEADERS-ONLY) | 0.0 / 0.25 / 0.5 |
| Confidence std (rule / learned, min across seeds) | 0.375 / 0.389 |
| ECE (rule [boot CI] / learned) | 0.0803 [0.0722, 0.0883] / 0.0518 |

Observed per-family diagnostics confirm the alias-OOD task design: no single channel reproduces pooled performance, and the URL channel alone resolves nothing (the leakage guard of the frozen design).

## 3. Derived Measurements

From raw rows, using the packet's RAW → DERIVED separation (all formulas frozen in spec/prereg):

- **G0 learned-vs-rule gap (paired alias tasks):** correct gap **0.0** (≤0.10), abs ECE gap **0.0285** (≤0.05), seed CV **0.0** (≤0.5), min confidence std across seeds **0.3887** (>0.05), pooled correct ≥0.50 (**40/40**), binomial vs 0.10 **p = 1.0e-40** (<0.05), McNemar vs B-EXACT-MATCH **p = 6.98e-10** (<0.05). → **G0 PASS**; no falsifier threshold triggered.
- **Rule proxy (replication of parent ceiling):** alias 1.0, FA 0.0, ECE 0.0803 (bootstrap CI [0.0722, 0.0883]), S1–S7 all pass.
- **Learned gates:** S1 pooled 1.0 + orthogonal 1.0 + mixed 1.0 (≥0.50/≥0.50/≥0.40) · S2 FA 0.0 ≤0.15 and 1.0 below verbatim's FA with McNemar p=7e-10 · S3 exact-match 12/12 (≥0.90) · S4 no-app/empty precision 1.0, ECE 0.052 ≤0.15 · S5 beats every retrieval baseline (all 0/40) → **all pass**.
- **Sequenced rule:** controls pass AND rule S1–S7 pass AND G0 pass AND learned S1–S5 pass ⇒ **SEQUENCED SURVIVES_CURRENT_TEST**.

## 4. Decision Assessment

Frozen outcome mapping (spec.json `decision_rule`):

| Component | Required | Observed | Pass |
|---|---|---|---|
| Controls PC-EXACT-MATCH / NC-NO-APPLICABLE / NC-EMPTY | all pass | 1.0 / 1.0 / 1.0 | ✅ |
| Rule S1–S7 | all | all | ✅ |
| G0 learned gate (gap≤0.10, |ECE gap|≤0.05, CV≤0.5, conf std>0.05, pooled≥0.50, binom p<0.05, McNemar p<0.05) | all | ✅ (gap 0.0, 0.0285, 0.0, 0.389, 40/40, 1e-40, 7e-10) |
| Learned S1–S5 | all | all | ✅ |

**Result: COMPLETE / SUPPORTS.** Consequences (as preregistered): the learned gate contributes to validating the critiquer-reconstructor pathway: alias-OOD resolution need not be a hand-written rule; a small learned adapter trained on a leak-free standard subset reproduces the synthetic ceiling and is well-calibrated. The claim ceiling is **bounded**: synthetic pooled 40 (30 orthogonal + 10 mixed) + held-out/mixed generalization; live web behavior remains untested (substrate unavailable) and LLM-scale GRPO untested (CPU-only runner).

## 5. Comparison with Parent (EXP-FRONTIER-35766532429)

- Parent's rule-proxy ceiling is **replicated exactly** (40/40, FA 0.0, ECE 0.0803, S1–S7) on a byte-identical fixture — the validated base stands.
- Parent's B-EXACT-MATCH/B-VERBATIM-REPLAY/B-RAG-TFIDF/B-RANDOM baselines replicate (0/40; verbatim FA 1.0). **New in this run:** B-RAG-EMBED (real all-MiniLM-L6-v2 retriever, threshold 0.60) → 0/40 alias success (220 encodings, 0.029 s/task) — retrieval alone is dominated by reconstruction, and the learned adapter beats it with 70 policy forwards and 7.9e-05 s/successful-alias-task.
- New capability evidence vs parent: the **learned** arm (parent had no learned mechanism) reaches the ceiling from 21 leak-free tasks, with calibrated model-derived confidence.

## 6. Product Consequences

No product promotion. Consequences for the frontier program:

- **Supports** (bounded): a learned System-One adapter can replace the hand-written rule for synthetic alias-OOD resolution with equal correctness, zero false-accepts, better ECE (0.052 vs 0.080), and 4x lower per-success latency in-process — with all the usual synthetic-to-real caveats.
- **Do not infer**: any statement about real-web targeted-exploration gains. Live BrowserGym WebShop/ALFWorld economics (browser/network work, false accepts under organic aliasing) are unmeasured; LLM-scale GRPO behavior unmeasured.
- **Next cheapest high-information step** (for the Director): obtain a runner with browsergym-webshop/alfworld packages + playwright browsers to execute the frozen live stratum; or extend the synthetic DGP with organic-aliasing statistics before further claim growth.

## 7. Validity Notes

See `result.json:validity_notes` (identical set). Highlights: learned arm is compact MLP GRPO, not LLM-scale (disclosed per spec); live stratum structurally unavailable (PC-BROWSERGYM-HEALTH not exercised — environment limitation, not a negative); learned confidence on no-candidate tasks is structural (RULE-mirror abstain constant) — the no-app/empty strata contribute partially non-model-derived confidence to ECE; learned ECE has no bootstrap CI; a first buggy run (GRPO gradient bug: whole-group log-prob scalar × mean-centered advantage ≈ zero gradient → LEARNED 0/40 constant conf) was fixed (per-member log-prob vector) and re-executed — the buggy numbers are excluded from this evidence base; all statistics are on the deterministic frozen task fixture; economics are in-process only.

## 8. Unresolved Questions

1. Transfer of learned-alias resolution to organic real-web alias formation (needs live substrate).
2. LLM-scale GRPO vs compact adapter on the same gates.
3. Learned ECE stability (no resampled CI).
4. Fully model-derived calibration on abstention strata.
5. End-to-end economics with browser/network work.
6. Composition limits of the shared per-slot adoption head (>3 slots, >3 channels).

## 9. Artifacts

| Path | Role |
|---|---|
| `research/experiments/EXP-FRONTIER-35773143736/raw_evidence.json` | Raw (610 per-task rows) |
| `research/experiments/EXP-FRONTIER-35773143736/raw_evidence_learned_seeds.json` | Raw (per-seed training/eval) |
| `research/experiments/EXP-FRONTIER-35773143736/tasks.json` | Fixture (identical to parent) |
| `research/experiments/EXP-FRONTIER-35773143736/train_split_inventory.json` | Derived (leak audit) |
| `research/experiments/EXP-FRONTIER-35773143736/derived_metrics.json` | Derived (all metrics incl. decision_components) |
| `research/experiments/EXP-FRONTIER-35773143736/learned_training_report.json` | Derived (training curves) |
| `research/frontier/run_genuine_35773143736.py` | Code (execute script) |
| `research/experiments/EXP-FRONTIER-35773143736/{spec.json, prereg.md, request.json, freeze.json}` | Frozen inputs |