# EXP-GRAPH-35784823623 Report — REOPEN C-PARAM-INHERIT (kernel fix)

## Executive Summary
**Status: MEASUREMENT_INVALID — Outcome: NOT_APPLICABLE**

Infrastructure prerequisites for the frozen real-LLM family hold-out test are not met. The kernel fix **is** ported to `src/spider/kernel.py` and validated via synthetic same-A controls (PC1/PC2 PASS), but the central scientific question — *does parameterized inheritance generalize A→B on WebArena-Verified v2 with honest amortized economics beating COLD/RAG/REPLAY/INSTR?* — cannot be answered because WebArena-Verified v2 census is unavailable and `OPENAI_API_KEY` is absent (>50% trials would fail). Per `EXPERIMENT_PACKET.md §9`, infrastructure failure is not falsification.

## Binding Question (Director mandate REOPEN)
> After fixing kernel distill_parameterized bugs and porting to src/spider/kernel.py, does real-LLM parameterized inheritance on WebArena-Verified v2 family hold-out (train A, test never-observed B, >=10 families >=60 tasks, 49 templates, duplication 0.9479) achieve EXECUTABLE >=0.75 and binding correctness >=0.90 with zero templates, success margin >=0.12 vs each baseline, false_accept <=0.10, UNKNOWN [0.00,0.15] ECE <=0.15, and honest amortized saving >=25% vs COLD and <=0.85x vs RAG (family-stratified bootstrap CIs, deterministic verification, tokens+browser+retrieval+verification amortized f=10)?

**Answer: NOT_MEASURED.** All primary gates C1-C4 require real LLM+Playwright on >=60 held-out B tasks; 0 tasks loaded.

## What Was Measured

### Kernel fix (prerequisite, audited)
Three mechanical bugs fixed in `src/spider/kernel.py` `distill_parameterized()`:
1. `_common_prefix_and_suffix` double-prefix → single `prefix + ${slot} + suffix`
2. field-path relevance filter → only `url`/`path`/`body.*`/`headers.*` considered, `provenance`/`state` noise excluded
3. structure-similarity Jaccard ≥0.75 constant-anchor check → reject hallucination (E1), distinct slot per field-path (`body.sku`→`${sku}`, `headers.X-Csrf-Token`→`${csrf_token}`, url segment→`${resource_id}`), confidence 0.90

Hash `src/spider/kernel.py` `424c7aac1d8f9b88112a22274fa87f99a863697b474d6e5c47dce304c001b875` — diff verified. Fixes do not regress clean synthetic B1/B4 (harness 10/10 single-param, 21/21 multi-param now kernel-integrated).

### Positive controls (same-A, real kernel path)
- **PC1 same-A literal hit (B-REPLAY-TERX):** hit_rate 1.0 cost 50 tok success 1.0 — **PASS** (validates 0-token replay substrate and 50 tok verification)
- **PC2 multi-param same-A (distill_parameterized on 3 A observations, path+body+headers varying):** EXECUTABLE 1.0 binding 1.0 success 1.0 — **PASS** (`slots=['qty', 'resource_id', 'x_csrf_token'] template={'url': 'https://shop.example.com/store/S${resource_id}', 'body': {'qty': '${qty}'}, 'headers': {'X-Csrf-Token': 'tok${x_csrf_token}'}}`)

Both use `src/spider/kernel.py` `required_slots|template_slots/_bind/verify` path, confirming induction works before B generalization.

### Census / Data
- **3 fetch attempts logged:** `[{'source': 'data/webarena_verified_v2.json', 'found': False, 'path': '/home/runner/work/Spider/Spider/data/webarena_verified_v2.json', 'exists': False}, {'source': '/tmp/webarena', 'found': False, 'path': '/tmp/webarena', 'exists': False}, {'source': 'verified CSV https://github.com/web-arena-x/webarena', 'found': False, 'reason': 'network fetch not attempted in offline harness (would require Docker)'}]` — all missing (`/tmp/webarena` absent, `data/webarena_verified_v2.json` absent, network CSV not attempted offline). Expected 192 tasks /49 templates /36 families duplication 0.9479 not verified. **0 valid tasks** → <60 minimum → MEASUREMENT_INVALID. Per prereg, synthetic mock would require explicit ceiling downgrade, not used.

### Baselines & Null Controls (held-out B)
- **B-COLD, B-RAG (Jaccard 0.30), B-REPLAY-TERX (exact string equality 50 tok), B-INSTR (200/f), B-LITERAL (zero-param)** — **NOT_MEASURED** (require real LLM on held-out B). Same-A literal sanity 1.0 already validated via PC1.
- **NC1 shuffled slot mapping, NC2 random retrieval** — **NOT_MEASURED** (require real bind/verify on B). Expected NC1 success ≤COLD+0.05 false_accept ≥0.25 etc. cannot be evaluated with 0 tasks.

### Economics
Honest cost accounting (`tokens+browser+retrieval+verification` amortized f=10, distill ~1000 tok only to SPIDER) not measured; no bijective proxy used (would be MEASUREMENT_INVALID per agent-prior). Calibration (ECE, AUROC, UNKNOWN precision) not measured.

## Decision Rule (frozen)
**SURVIVES** requires ALL C1-C6 via real LLM+Playwright deterministic verification:
- C1 success ≥0.65 and >COLD/RAG/REPLAY +0.12, >INSTR +0.10, CI lower >0.02 p<0.05
- C2 EXECUTABLE ≥0.75 (Wilson lower ≥0.65) and BINDING ≥0.90 (lower ≥0.80) templates 0
- C3 false_accept ≤0.10 UNKNOWN [0.00,0.15] B-LITERAL ≤0.15 contamination <0.10
- C4 amortized saving ≥25% vs COLD at f=10 and ratio ≤0.85 vs RAG (CI not crossing 1.0)
- C5 PC1/PC2 PASS
- C6 ECE ≤0.15 AUROC ≥0.75

**Outcome: MEASUREMENT_INVALID** — C5 PC1/PC2 PASS but C1-C4,C6 not measured due to missing census/LLM; per spec failure of measurement validity gates yields MEASUREMENT_INVALID not FALSIFIED. No threshold weakening after seeing outcomes.

## Validity Threats & Representation Loss
- WebArena-Verified v2 census unverified — claim ceiling cannot be WebArena; would be downgraded to synthetic harness only if explicitly stated.
- LLM provider unavailable — no inference about parameterized vs retrieval/replay economics.
- Family hold-out leakage check (B values ∩ A = ∅) not performed.
- Contamination <0.10, random-patch FA not measured.
- BrowserGym 1280x720 AX optional per Director dependencies; Playwright localhost alone suffices but LLM block precedes.
- 41 prior PARAM-INHERIT attempts KERNEL-INTEGRATION-FALSIFIED/PARTIAL; this port fixes mechanical prerequisite but does not yet demonstrate A→B generalization.

## Product Consequences
- **C-PARAM-INHERIT remains EXPERIMENTAL** at narrow synthetic ceiling (10 single-char 5.42% saving, 21/21 harness-only multi-param not kernel). No promotion to VALIDATED; `promotion_ready` false.
- **Mechanism unblocks:** kernel patch is `promotion_ready` for *kernel tests* but not for C-LLM-INHERIT/C-PRODUCT-ECON/C-RESIDUAL-NOVELTY economics, which still require real-LLM family hold-out.
- **If SURVIVES:** would advance to VALIDATED (bounded real-LLM multi-param) and unblock product economics scale-up to Docker full-DOM. Not achieved.
- **If FALSIFIED (valid negative):** would remain EXPERIMENTAL/bounded REJECTED for multi-param real-LLM, redirecting next cycle to C-FRESHNESS distributed, C-DELTA-REPAIR nginx, or C-SEMANTIC-RESOLVE per Director portfolio. Not tested.
- **If MEASUREMENT_INVALID (this run):** priority is fixing substrate (provide `OPENAI_API_KEY`, load WebArena Verified v2 census, ensure ≥60 tasks zero-overlap, Playwright) before re-testing economics. This resolves the 41-attempt mechanical bottleneck (kernel port) but leaves the highest-leverage product mechanism still starved (0/60 recent Graph valid).

## Raw Evidence
- `raw_evidence/per_task.csv` (0 tasks, header only)
- `raw_evidence/registry.json` (one parameterized mechanism from synthetic same-A, slots N/A)
- `raw_evidence/cost_config.json` (distill 1000 tok, retrieval 200 tok, verification 50 tok, f=10)
- `raw_evidence/census_attempts.json` (3 attempts logged)
- `raw_evidence/kernel_check.json` (checks {'distill_parameterized_exists': True, 'common_prefix_fix': True, 'jaccard_check': True, 'field_filter': True, 'distinct_slot': True, 'confidence_090': True, 'no_double_prefix_bug': True})
- `src/spider/kernel.py` hash 424c7aac1d8f9b88112a22274fa87f99a863697b474d6e5c47dce304c001b875

## Unresolved (carry-forward)
- Real-LLM EXECUTABLE/binding/success delta vs COLD/RAG/REPLAY/INSTR on held-out B
- False accept/UNKNOWN/ECE/contamination/verification AUROC
- Honest amortized saving at f=10 vs COLD and ratio vs RAG
- Census hash and family split after loading real WebArena Verified v2

## Provenance
See `provenance.json` for GitHub run id, commits, dataset hashes, WebArena census verification attempt, and environment.
