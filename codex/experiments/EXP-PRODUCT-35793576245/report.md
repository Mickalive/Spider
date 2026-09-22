# EXP-PRODUCT-35793576245 — EXECUTE report (claim C-RESIDUAL-NOVELTY)

**Status:** COMPLETE — **Outcome:** FALSIFIES

## Summary

Honest branch-derived amortized cost (f=10) of SPIDER parameterized inheritance vs strong
baselines on the WebArena-Verified v2 file-based census (192 tasks / 36 families >=3 /
49 templates; train pool A, test never-observed pool B; novelty levels 0/25/50/75/100%).

Primary statistic: Spearman rho_novelty = 0.608
(block-permutation p = 0.0002, family-stratified
bootstrap 95% CI 0.480..0.717).
R2_delta = 0.400 (R2_novelty 0.509,
R2_length 0.110). Per-stratum |rho_length|:
{'0.0': 1.0, '0.25': 0.366, '0.5': 1.0, '0.75': 1.0, '1.0': 1.0}.

## Decision criteria
C1 correctness+calibration: True
C2 positive controls: True
C3 novelty tracking: True
C4 residual explanatory power: False
C5 work compression honest: False
C6 null controls: False

## Why
C2 passed: TERX and Stagehand hit_rate 1.0 at n=0 (TERX 50 tok verify-only, success 1.0);
SPIDER binding correctness 1.0 at n=0 via actual _bind. C1 passed: SPIDER success 1.0 at n=0
(Wilson lower 0.904), false_accept
0, UNKNOWN_precision 1.0, ECE(exec) 0.025,
confidence std 0.405. C3 passed:
rho_novelty strongly positive with CI lower > 0.35. C5 failed: SPIDER/COLD at n=0 =
0.163 (saving present) but SPIDER is NOT cheaper than
B-RAG-EMBED at n=0 (1.126x) nor within 1.20x of
B-STAGEHAND-CACHE (1.503x) and is more expensive than
TERX's COLD fallback at n>=0.5 (SPIDER abstains -> COLD+300). C4 failed: R2_delta
0.400 < 0.50 and per-stratum rho_length ~1.0 (every branch
scales with steps; see validity_notes). C6 failed strictly: NC1-SHUFFLED rho = 0.313
exceeds the |rho|<0.25 null bound (block-permutation p = 0.0002): the abstention schedule
itself (UNKNOWN gate) correlates with novelty, so the shuffled control is not perfectly flat;
NC2 (rho 0.005) and NC3 (rho 0.005) are flat. NC1 rho stays below the 0.35
measurement-invalidation bound, and C6 does not change the FALSIFIES precedence (C5 fail
dominates).

## Interpretation
- Under the frozen precedence, C5 failure implies FALSIFIED (no honest saving vs strong
  baselines). An alternative MIXED reading — correct and genuinely novelty-tracking (C3) but
  with constant overhead (retrieval 200 + distill 100) dominating the savings edges — is
  documented; both readings agree the commercial promise 'pay only residual novelty' is not
  met under this kernel/cost model on this census.
- SPIDER DOES track residual novelty (rho 0.608) — the
  mechanism economics work when identifiers are pre-known — but fixed amortization and
  abstention-to-COLD make it non-competitive with pure retrieval-replay at exact repeat and
  with COLD at high novelty under the frozen constants. The NC1 signal (0.313) further
  locates the tracked gradient in the abstention schedule rather than in slot binding per se.
- No promotion. Product consequence follows the frozen negative branch: park pay-for-novelty
  economics for this kernel/cost model; prioritize caching/freshness/delta-repair; revisit
  parameterized inheritance only with a cost model that does not double-charge fixed
  retrieval+distill versus zero-overhead replay baselines.

Artifacts: fixtures/tasks.json, artifacts/registry.jsonl, artifacts/raw_per_task.csv,
artifacts/branch_traces.json, artifacts/derived_metrics.json, artifacts/cost_config.json.
