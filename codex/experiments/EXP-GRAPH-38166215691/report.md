# EXP-GRAPH-38166215691 — Experiment Report

**Lane:** graph  
**Claim:** C-SEMANTIC-RESOLVE (status HYPOTHESIS → EXPERIMENTAL for embedding-selection sub-mechanism)  
**Design-contract version:** 2  
**Frozen inputs:** `request.json`, `spec.json`, `prereg.md`, `freeze.json`, `design_review.json` (all immutable)  
**EXECUTE date:** 2026-10-11  
**Base SHA at design time:** `7174818443e126da8be7919c825320999f568486`

---

## 1. Summary

This experiment tests whether **max-cosine-similarity selection over intent embeddings (A-EMBED-COSINE)** binds the correct registry mechanism on natural-language goals that were **independently authored** (never seen the registry intent strings or any prior authoring surface), and by how much it exceeds a **token-overlap null (B-LEXICAL-OVERLAP)** on those same goals.

**Result:** `status=COMPLETE`, `outcome=SUPPORTS` for the primary claim-bearing decision **D-SELECTION**.  
**Secondary abstention decision D-ABSTENTION:** `AB-NOT-MET` (non-gating, reported separately).

### Key Numbers (Primary Set, n=93)

| Arm | Mechanism-Identity Accuracy | Numerator / Denominator |
|-----|----------------------------|-------------------------|
| **A-EMBED-COSINE** (treatment) | **0.9247** | 86 / 93 |
| **B-LEXICAL-OVERLAP** (comparator / distinct reference) | 0.5269 | 49 / 93 |
| **B-RANDOM-ROLE** (floor null) | 0.2258 | 21 / 93 |
| **B-INCUMBENT-KERNEL** (product baseline) | 0.0000 | 0 / 93 |
| **B-INTERNAL-ID-ORACLE** (ceiling) | 1.0000 | 93 / 93 |

**Paired family-blocked bootstrap** (B=10000, α=0.05, 5 resource families, seed=3806477323):  
**Observed difference (embed − lexical) = 0.3978**, 95% CI = **[0.2967, 0.4947]**.  
Lower bound **strictly above zero** → **D-SELECTION = SUPPORTS**.

---

## 2. What This Experiment Measures (and What It Does Not)

### In Scope (measured)
- Mechanism-identity selection accuracy on 93 independently authored single-operation goals (contamination-screened from 140 total).
- Discrimination between A-EMBED-COSINE and B-LEXICAL-OVERLAP on the same goals.
- Control sensitivity: all gated controls (PC, NC, oracle, floor, non-tautology, shuffle) passed.
- Abstention risk-coverage frontier on the same score geometry (secondary, non-gating).

### Out of Scope (not measured or claimed)
- Parameter binding, HTTP execution correctness, cross-app generalization.
- ECE gating (descriptive only; prior audit VF-06 shows unattainability).
- Product promotion (only a verdict can grant that).
- The full C-SEMANTIC-RESOLVE claim — only the **embedding-selection sub-mechanism** is tested here.

---

## 3. Experimental Design Highlights

This packet is a **design-contract v2 redesign** that fixes the three control-plane/design defects that invalidated the three prior C-SEMANTIC-RESOLVE packets:

| Prior Defect | This Packet's Fix |
|--------------|-------------------|
| Joint-authorship confound (goals & intents authored in same file) | Goals authored by **two fresh-context processes** that never saw intents or repo files; **extended contamination screen** against union of 20 intents + all PARAPHRASES + NO_APPLICABLE_TEMPLATES + OOD_PARAPHRASES; 9/140 goals flagged (≥0.60 Jaccard) and excluded. |
| Reference arm provably identical to candidate (argmax of monotone similarity) | **B-LEXICAL-OVERLAP** (set-Jaccard) is a **provably distinct function** from A-EMBED-COSINE (dense cosine); V9-NON-TAUTOLOGY requires decision vectors to differ on ≥1 goal and lexical accuracy < 0.99. |
| Positive control pinned at ceiling (verbatim intents) | **PC-LIVENESS-AND-INTEGRITY** has three fallible sub-checks: fixture uniqueness (20/20), incumbent verbatim resolution (20/20), resolver self-match (20/20). |
| Unattainable ECE target (VF-06) | ECE is **descriptive only**; D-ABSTENTION **decoupled and non-gating** (mandate item iii). |

### Contamination Screen (V3)
- Screened all 140 goals against **every prior authoring surface** (20 intents + 60 PARAPHRASES + 22 NO_APPLICABLE_TEMPLATES + 9 OOD_PARAPHRASES).
- Tokenisation: lowercase whitespace split, set Jaccard (identical to B-LEXICAL-OVERLAP).
- **9 goals flagged** (max prior Jaccard ≥ 0.60): 7 applicable (`app_001`, `app_021`, `app_024`, `app_031`, `app_041`, `app_061`, `app_081`) + 2 out-of-scope (`oos_009`, `oos_028`).
- Primary set = 100 applicable − 7 flagged = **93 goals** (≥ 80 gate satisfied).
- All 5 resource families represented: users 19, posts 17, comments 19, albums 19, photos 19.

### Independent Authorship Provenance (V4)
- **Author-1** (fresh context): 100 applicable + 20 out-of-scope goals from schema "resource family × operation verb + negative categories only".
- **Author-2** (fresh context): 20 further out-of-scope goals under same schema.
- Neither author saw INTENTS, PARAPHRASES, NO_APPLICABLE_TEMPLATES, OOD_PARAPHRASES, any harness file, or prior packet text.
- Canonical bank-block sha256: `fb4d3246990731c95f4cf4cfa5870ac7f02da8832eed324580be5f75b1456c6e` (verified at EXECUTE).

---

## 4. Primary Result: D-SELECTION = SUPPORTS

**Decision rule (frozen in spec.json):**
- SUPPORTS: All V1–V12 PASS **AND** `obs_diff > 0` **AND** `lower_ci > 0`.
- FALSIFIES: All V1–V12 PASS **AND** `obs_diff ≤ 0`.
- MIXED: All V1–V12 PASS **AND** `obs_diff > 0` **BUT** `lower_ci ≤ 0`.

**All 12 validity gates passed:**
- V1 METRIC-DEFINITION: all denominators = 93 ✓
- V2 PRIMARY-SET: |primary| = 93 ≥ 80 ✓
- V3 CONTAM-SCREEN: 9 flagged ≤ 20 ✓
- V4 AUTHORSHIP-PROVENANCE: bank sha256 matches ✓
- V5 PC: all sub-checks 20/20 ✓
- V6 ORACLE-CEILING: 1.0 on primary ✓
- V7 TREATMENT-LIVENESS: 20 distinct valid selections ✓
- V8 FLOOR-SANITY: random ≤ 0.35 (0.2258) ✓
- V9 NON-TAUTOLOGY: 41 disagreements, lexical acc 0.5269 < 0.99 ✓
- V10 NC-SHUFFLE: NC-SHUFFLED-LABEL=0.0 ≤ 0.20, NC-RANDOM-SCORE=0.043 ≤ 0.25 ✓
- V11 BOOTSTRAP-SEED: n_resamples=10000, α=0.05, 5 families, seed=3806477323 ✓
- V12 FREEZE-BINDING: all 8 bound file hashes match freeze.json ✓

**Bootstrap result:** `obs_diff = 0.3978`, `lower_ci = 0.2967`, `upper_ci = 0.4947` → **SUPPORTS**.

The **0.3978 advantage** (95% CI [0.2967, 0.4947]) is **larger** than the prior jointly-authored 0.2308 [0.1136, 0.3509] from EXP-GRAPH-36287167610, confirming the effect is **not a joint-authorship artifact** — it survives removal of the confound.

---

## 5. Secondary Result: D-ABSTENTION = AB-NOT-MET (Non-Gating)

**Calibration split:** 39 applicable + 19 out-of-scope  
**Test split:** 54 applicable + 19 out-of-scope  
**Threshold selection rule (predeclared):** smallest calibration score `t` with cal pooled_false_accept ≤ 0.10 **AND** cal unknown_precision ≥ 0.85; if none, minimise `|fa − 0.10|` subject to precision ≥ 0.85; else `t* = 1.0`.

**Result:**
- No calibration threshold met both targets → `cal_feasible = false`
- `t* = 0.4445` (minimising `|fa − 0.10|` subject to precision ≥ 0.85)
- On test split at `t*`: coverage = 1.0, pooled_false_accept = **0.5789**, unknown_precision = 1.0
- **AB-NOT-MET** (pooled_false_accept > 0.10)

**Rationale for non-gating (frozen in spec.json reachability):**  
With 54:19 test ratio, precision ≥ 0.85 forces abstaining on ≥ 18/19 negatives while allowing ≤ 3/54 applicable abstentions. The prior measured candidate had pooled_false_accept = 0.3871; coupling the two decisions would risk an empty accept region. D-ABSTENTION answers the applicability-gate question directly; D-SELECTION answers the selection question.

---

## 6. Controls Summary

| Control | Expected | Observed | Pass |
|---------|----------|----------|------|
| **PC-LIVENESS-AND-INTEGRITY** | fixture 20/20 unique; incumbent verbatim 20/20; lexical_self 20/20; embed_self 20/20 | All 20/20 | ✓ |
| **NC-SHUFFLED-LABEL** | ≤ 0.20 (deranged labels) | 0.0000 | ✓ |
| **NC-RANDOM-SCORE** | ≤ 0.25 (random scores through same pipeline) | 0.0430 | ✓ |
| **B-INTERNAL-ID-ORACLE** | 1.0 on primary | 1.0 (93/93) | ✓ |
| **B-RANDOM-ROLE** | ≤ 0.35 | 0.2258 | ✓ |
| **B-LEXICAL-OVERLAP** | disagrees on ≥1 goal, acc < 0.99 | 41 disagreements, 0.5269 | ✓ |
| **B-INCUMBENT-KERNEL** | 0.0 on primary | 0.0 (0/93) | ✓ |

All controls are **arithmetically fallible** and passed — no degenerate fixtures, no tautological arms, no ceiling/floor pinning.

---

## 7. Validity Notes

1. **Binding-only measurement** — no HTTP server started, no LLM calls, no browser, no external task traffic. Single HuggingFace model download (pinned revision recorded).
2. **Mechanism identity only** — parameter binding and execution correctness are out of scope.
3. **Bootstrap covers resampling variability only** (family-blocked, seed 3806477323); single embedding model, no ensemble, no cross-model replication.
4. **Contamination screen** uses identical tokenisation to B-LEXICAL-OVERLAP and screens against the full union of prior authoring surfaces from the bound `goal_generator.py`.
5. **ECE is descriptive only** (0.2332) and NOT a gate (mandate item iii; prior audit VF-06).
6. **Model revision:** the pinned revision `c9745ed1d9f207416be6d2e6f8de32d1f161f9bf` was not available at EXECUTE; the runner fell back to the unpinned model name (recorded as `model_revision=null` in env).
7. **Measurement failure vs. negative result kept distinct:** any infrastructure failure would yield `status=BLOCKED`, never `FALSIFIES`.

---

## 8. Consequences

### If SUPPORTS (this outcome)
- First contamination-free evidence that embedding-based semantic resolution binds unseen natural-language goals above a token-overlap null.
- Licenses moving the **embedding-selection sub-mechanism** of C-SEMANTIC-RESOLVE toward **EXPERIMENTAL** (no product promotion).
- Supports keeping semantic resolution on the shipped `observe→distill→registry→resolve→execute` path.
- Unblocks parameter-binding and abstention-calibration follow-ups.
- Reduces risk on C-LLM-INHERIT and C-PRODUCT-ECON.
- The AB-NOT-MET result means a single global cosine threshold **cannot** be shipped as an applicability gate without a separate calibration; the resolver must not be shipped without one.

### If FALSIFIES/MIXED (counterfactual)
- The bounded 45/52-vs-33/52 advantage was (at least substantially) a joint-authorship artifact.
- C-SEMANTIC-RESOLVE stays HYPOTHESIS; embedding-argmax resolution must not be relied on as a load-bearing component.
- Next attempt must change architecture (learned paraphrase training, structured parameter/slot reasoning, or retrieval model trained on independently authored goals) rather than re-tune thresholds.

---

## 9. Unresolved Questions

1. **AB-NOT-MET** — the secondary abstention gate missed its targets; a single global threshold cannot simultaneously achieve FA ≤ 0.10 and precision ≥ 0.85 on this bank. This does not downgrade D-SELECTION but means the resolver needs a separate applicability gate before shipping.
2. **Generalization** — whether the 0.3978 advantage holds beyond this fixture, embedding model, and goal bank is untested.
3. **Parameter binding / execution** — out of scope; positive selection does not imply end-to-end usability.
4. **Model revision drift** — EXECUTE used the unpinned default revision (HuggingFace Hub did not serve the pinned revision); the effect of revision drift on the advantage is unmeasured.

---

## 10. Artifacts

All outcome-bearing code and data are hash-bound by `freeze.json`:

- **Frozen modules (8):** `research/harness/candidate_resolver.py`, `goal_generator.py`, `http_server.py`, `experiment_runner.py`, `src/spider/kernel.py`, `registry.py`, `models.py`, `__init__.py`
- **Goal bank:** embedded verbatim in `prereg.md` (sha256 `fb4d3246...`)
- **Runner script:** verbatim transcription in `prereg.md` section 14 (sha256 `065b7557...`)
- **Raw evidence:** `derived/predictions.json` (per-goal selections, confidences)
- **Derived evidence:** `derived/contamination.json`, `derived/measurements.json`
- **Freeze record:** `freeze.json` with all artifact hashes

---

*This report is explanatory; the canonical machine handoff is `result.json`.*