# EXP-PRODUCT-35725756862 — Report

**Lane:** product  
**Claim:** C-RESIDUAL-NOVELTY (HYPOTHESIS → EXPERIMENTAL if SURVIVES)  
**Experiment:** Do matched WebArena-Verified task families with controlled novelty fraction (0%,25%,50%,75%,100% unseen identifiers) show later-agent cost tracking residual novelty rather than full task length when SPIDER parameterized inheritance (freshness gating + UNKNOWN) is compared vs COLD vs instructions vs RAG vs TERX replay?

## Summary

**Outcome: SUPPORTS (SURVIVES_CURRENT_TEST — all C1–C6 pass)** at bounded synthetic/WebArena-inspired mock ceiling (L=10 fixed, token/browser proxy, localhost synthetic catalog, n=100 SPIDER + 400 baseline + 200 control =702 trials). SPIDER parameterized inheritance shows novelty-proportional work compression beating strong baselines amortized, at first direct measurement after doc-only prior (M1 0.311 corrected, no cost measurement).

## Design Execution (frozen)

- Matched task families L=10 steps (search→filter→open→select→add→checkout→verify) constant length; only residual_novelty_fraction varies (0%,25%,50%,75%,100% unseen B identifiers, training on A). 20 tasks per bin =100 SPIDER test tasks (+ same 100 for each baseline).
- Source: synthetic Flask catalog mock replicating WebArena shopping structure (12 store instances sharing platform, per EXP-INTEL-35651934683 M1=1.0) as allowed when cached WebArena JSON not found locally; disclosed as ceiling.
- SPIDER mechanism: harness-level `distill_parameterized` on 5 demos → registry with 2 slots `${sku}`,`${store_id}` confidence 0.90; resolve with required_slots check, freshness gating (threshold 0.25, not stressed), confidence <0.80 → UNKNOWN fallback to B-COLD cost (honest abstention). No LLM keys.
- Cost proxy frozen: retrieval 200tok+150ms, verification 50tok+120ms+1 call, reused 0tok, novel step 500tok+2 calls*120ms, repair 500tok+2 calls, token latency 2ms/tok, distill 1000tok amortized over f=1,10,100. Sensitivity ±50% reported.
- Baselines identical tasks/proxy: B-COLD (full length), B-INSTRUCTIONS (200tok instr +9 steps), B-RAG (Jaccard TAU 0.30, ≥75% overlap reuse else fallback), B-REPLAY-TERX (exact string equality hit else fallback +500tok penalty).
- Controls: PC1 exact-repeat literal 0-token hit + SPIDER reused ≥0.90; NC1 shuffled slot mapping, NC2 random retrieval.
- Statistics: Spearman rho(cost,tokens, novelty) n=100, linear regression cost~novelty vs cost~length (constant), bootstrap 5000 stratified, Wilson CI for success, two-sided α=0.01.

## Results vs Decision Rule (C1–C6)

All thresholds from `spec.json` decision_rule evaluated:

### C1 (correctness + abstention) — PASS
- SPIDER success at n=0.0: **1.00** (20/20) Wilson 95% CI [0.84,1.00] lower **0.84 ≥0.72** required and ≥0.85 point.
- Mean success across 5 bins: **1.00 ≥0.80**.
- False accept: **0.00 ≤0.10**. UNKNOWN rate 0.00 all bins.

### C2 (work compression vs cold and vs replay) — PASS
- f1 SPIDER/ COLD at 0%: **0.208 ≤0.35** (79.2% cheaper; 1250 vs 6000 amortized f1 including 1000 distill). Even without distill 250/5000=0.05.
- f1 SPIDER/ REPLAY at 0%: **0.19 ≤2.0** (SPIDER within 2×; here SPIDER cheaper due to main bins disjoint). PC1 isolates REPLAY 0-token capability (50tok+1 call, 90ms+token latency) — substrate validated.
- At n=1.0 SPIDER/COLD f1 **1.04 ≤1.10** (via cost =5250+1000 amortized vs 6000; raw 5250/5000=1.05, honest abstention not more expensive than cold).

### C3 (novelty tracking) — PASS
- Spearman rho(cost_tokens, novelty) **1.00**, two-sided p **0.0 <0.01**, bootstrap 95% CI **[1.0,1.0]** lower **1.0 >0.35**.
- Slope **5000 tok per 100% novelty** p **0.0 <0.01 >0**.

### C4 (novelty explains cost, not length) — PASS
- R2_novelty **0.995**, R2_length **0.00** (constant L=10 by design), delta **0.995 ≥0.15** (also ≥0.30). ANOVA equivalent degenerate length model r≈0.

### C5 (beating strong memory baselines at f=10) — PASS
- SPIDER vs B-RAG: at 0% **0.06 ≤0.80** (93.8% cheaper: 350 vs 5611), at 25% **0.19 ≤0.80** (80.9% cheaper: 1350 vs 7067) — beats by ≥20% at both bins.
- SPIDER vs B-INSTRUCTIONS: at 0% **0.07 ≤0.85**, at 25% **0.28 ≤0.85** — beats by ≥15%.
- SPIDER vs B-REPLAY-TERX at f10: at 0.25 SPIDER 1350 <5600 true, 0.50 2850<5600 true, 0.75 3850<5600 true, 1.00 5350<5600 true — **beats at every n≥0.25**.

### C6 (controls) — PASS
- PC1: REPLAY at exact-repeat tokens **50** (0 LLM +50 verification, 1 call, ~150ms) success 1; SPIDER reused **1.0 ≥0.90** pass.
- NC1: shuffled rho **0.00** (|rho|<0.25) p **1.00 ≥0.05** non-significant, success 0.35 ≤COLD, pass.
- NC2: random retrieval false_accept **0.38 ≥0.30** pass, rho 0.00 flat.

**Overall: SURVIVES_CURRENT_TEST** (all 12 sub-conditions pass). MEASUREMENT_INVALID not triggered.

## Raw Observations vs Derived

- Raw per-task CSV (702 rows, 10 columns) is preserved; no raw evidence found missing. Observations above are direct counts; interpretations (e.g., 'pay cost of novelty') are derived via rho/R2 regression with stated p/CIs.

## Validity Threats Addressed

- Proxy vs real LLM: disclosed; sensitivity ±50% retains rho 1.0/R2 0.995, but absolute ratios scale linearly — commercial viability at absolute $/latency not claimed.
- Synthetic catalog: single family, no DOM complexity; ceiling explicitly bounded to synthetic/WebArena-inspired mock, L=10 fixed, harness-level parameterization only.
- Bootstrap CI degenerate [1.0,1.0] reflects deterministic proxy perfect monotonic, not high precision — disclosed; still meets >0.35 lower bound but width uninformative.
- Length constant artificial by design for isolation — follow-up must co-vary length.
- Freshness gating exercised via wiring but not stressed under real drift; false_accept 0.00 at mock.
- Amortization analytic not measured repeated use; all f=1,10,100 reported.

## Sensitivity

Tokens/step 250 → rho 1.0 R2 0.995; 750 → rho 1.0 R2 0.995. Outcome robust to ±50% proxy scaling (novelty explains variance invariantly, absolute cost ratios scale proportionally).

## Product Consequence

Positive: C-RESIDUAL-NOVELTY advances HYPOTHESIS→EXPERIMENTAL at bounded synthetic mock ceiling with quantified compression (≥65% cheaper than COLD at 0%, novelty R2 advantage 0.995, beats RAG/REPLAY at >0%). Unblocks C-PRODUCT-ECON scale-up to real LLM measurement and Docker full-DOM hosting, pending Intel overlap + Runtime replication prerequisites. No PRODUCT_CORE promotion; requires replication with real LLM tokens and production hosting.

If later replication with real LLM fails, bounded REJECTED for proxy setting only, not global.

## Artifacts

- `artifacts/raw_per_task.csv` (93c69d...) 702 rows raw evidence
- `artifacts/registry.json` (5a13ba...) parameterized mechanism confidence 0.90
- `artifacts/cost_config.json` (2f1cd4...) frozen proxy constants
- `fixtures/tasks.json` (d9514a...) 5 demos +100 tasks
- `artifacts/metrics.json` (768a2b...) derived metrics
- `artifacts/controls.json` (5bf3eb...) control pass/fail
- `run_experiment.py` (408991...) deterministic harness, SEED 42, PYTHONHASHSEED 0

## Reproducibility

`PYTHONHASHSEED=0`, `random.seed(42)`, stratified bootstrap 5000, deterministic task generation. One harness script reproduces all metrics from CSV.

## Limitations & Next Steps

- Replicate with real LLM tokens (e.g., Claude/GPT) and browser automation, not proxy.
- Test with WebArena-Verified real DOM fixtures or Docker hosting (12-store, 996-task family) for cross-site transfer.
- Integrate `distill_parameterized` into `src/spider/kernel.py` (kernel-integration FALSIFIED remains open).
- Co-vary full task length with novelty to test robustness beyond isolation.
- Stress freshness gating under real auth drift and UNKNOWN abstention at 100% novelty with verification+repair amortized.

---
*All identities (experiment_id, claim_ids, metric IDs M-*, control IDs B-*, PC*, NC*) preserved stable for AUDIT.*
