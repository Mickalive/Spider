# EXP-GRAPH-35741890679 Report: C-DELTA-REPAIR Localized Repair

## Question
After runtime's verified byte-preserving nginx HIT-cache substrate (oracle-free decompression 960/960 byte-identical across HIT/SWR/SIE/304 stages), does a controlled single-resource local perturbation require only localized repair versus full re-exploration, with repair cost amortized over retrieval frequency?

## Hypothesis
C-DELTA-REPAIR hypothesis: single-resource local perturbation is repairable by localized patch without full re-exploration. Predictions: (1) success >=80% pooled >=70% per-family, (2) repair tokens <50% cold and browser <40% cold, (3) verification AUROC>=0.75 prec>=0.80, (4) contamination <10%, (5) amortized cost at n=10 < cold.

## Substrate
Simulated nginx reverse-proxy HIT/SWR/SIE/304 with oracle-free gzip.decompress, verified 960/960=1.0000 byte-identical on 960 synthetic bodies (SHA256 HIT==SWR==SIE==304). Flask HS256 simulation, localhost, perturbation isolation single resource blast_radius=1, registry clone isolation, 36 instances (F-DOM 12, F-ENDPOINT 12, F-CACHE 12) x 6 seeds, TRAIN 18 / TEST 18 stratified, 24 unrelated mechanisms for contamination, deterministic hashlib seeds, verification threshold fit TRAIN evaluated TEST.

## Baselines
- B-COLD-FULL-REEXPLORATION: tokens 2244.2 browser 8.7 success 0.944 n=36
- B-VERBATIM-REPLAY: success 0.028 (1/36) near 0 as expected (breaking perturbations)
- B-RETRIEVAL-RAG: success 0.333 vs repair 0.833 delta 0.500 (repair exceeds retrieval by 50.0pp)
- B-ORACLE-HAND-PATCH: success 1.000 tokens 120 browser 1 ceiling within 2x
- B-RUNTIME-BYTE-IDENTITY: 960/960=1.0000 >=0.99 pass

## Controls
- PC1 unperturbed 1.000 n=12, PC2 oracle patch 0.917 token ratio 0.053 -> C1 PASS
- NC1 zero perturbation cost 0 contamination 0.0, NC2 distant contamination 0.0, random-patch false-accept 0.033 AUROC 0.667 -> C2 PASS
- C3 byte identity 1.0000 >=0.99 -> PASS

## Primary Results (frozen TEST n=18, holdout threshold from TRAIN)
- **C4 Success pooled TEST 0.944 CI (0.7424220019799247, 0.9901250641690756) vs 0.80: PASS, per-family TEST {'F-DOM': 1.0, 'F-ENDPOINT': 0.833, 'F-CACHE': 1.0} vs 0.70: PASS -> C4 PASS (all pooled 0.833 CI (0.6810888526532568, 0.9212965937143589))
- **C5 Cost TEST token ratio 0.613 CI (0.5693605808782, 0.6606153621162313) <0.50?False, browser ratio 0.431 CI (0.39609758076198764, 0.46915946250921153) <0.40?False, verif mean 1.44 <=2?True -> C5 FAIL (repair tokens 1364.1 vs cold 2226.4, browser 3.7 vs 8.6)
- **C6 Contamination mean 0.0046 max 0.0833 <0.10 -> PASS
- **C7 Verification TEST AUROC 1.000 >=0.75?True, precision 1.000 >=0.80?True, recall 1.000 -> C7 PASS (all AUROC 1.000, random null AUROC 0.667)
- **C8 Amortized TEST tokens 4744.1 vs cold 2226.4 FAIL, browser 17.1 vs 8.6 FAIL -> C8 FAIL (all tokens 4810.7, retrieval tokens 320 + verif 180)

## Decision
- C1 True C2 True C3 True -> measurement valid? True
- Primary C4 True C5 False C6 True C7 True C8 False -> all? False
- **Overall: status=COMPLETE outcome=FALSIFIES**

Frozen decision rule: CONFIRMED only if C1-C8 all PASS on TEST. Here C5 FAIL (token ratio 0.613 >=0.50, browser ratio 0.431 >=0.40) and C8 FAIL (amortized 4744.1 > cold 2226.4). C1-C3 pass, so valid negative (not infrastructure failure). C4/C6/C7 pass show functional repair succeeds with low contamination and strong verification, but bounded-cost claim falsified in this setting.

Per-family breakdown (all n=12, TEST n=6 each) shows heterogeneity but all families pass C4 (>=0.70) while C5 fails globally - not family-specific, so FALSIFIED-IN-SETTING not MIXED. The cheapest possible radius (single-resource) is not cheaper than cold when amortized: pay novelty 61% of whole task tokens before amortization, 2.2x after 10 reuses.

## Product Consequence
FALSIFIED-IN-SETTING: single-resource locality fails on cost even where functional repair succeeds (83% success). Product must budget repair ≈ cold cost and default to full re-exploration or RAG+fused fallback, not localized patch+verify loop. Prevents premature repair-layer promotion and contamination risk is low but false economy dominates. Graph lane should pivot to C-RESIDUAL-NOVELTY matched families or C-SEMANTIC-RESOLVE abstention calibration, per Director portfolio - bounded cost assumption not supported on nginx HIT-cache localhost synthetic perturbations.

## Effect Sizes and CIs
- Repair success Wilson 95% CI pooled all [0.681,0.921], pooled TEST [0.742,0.990], per-family CI width ~0.22 at n=12 (pre-reg adequacy note).
- Cost ratios bootstrap 2000 resamples by instance 95% CI tokens (0.5693605808782, 0.6606153621162313), browser (0.39609758076198764, 0.46915946250921153) (TEST holdout).
- Verification AUROC 1.000 precision 1.000 recall 1.000 at threshold 0.6 (TRAIN fit).

## Validity Notes
Simulated substrate not real nginx, synthetic DOM/headers, heuristic repair not real LLM, Playwright actions counted not executed, localhost only, single model, underpowered per-family TEST n=6 (exploratory). See validity_notes in result.json.

## Artifacts
- raw_evidence/experiment_data.json (instances, repair_results, cold costs, verification arrays)
- raw_evidence/metrics.json (derived metrics)
- raw_evidence/byte_identity.json (960 byte identity sample)
- raw_evidence/perturbation_manifest.json (36 manifests)
- raw_evidence/repair_results.json (per-instance)
- research/graph/delta_repair/execute_delta_repair.py (code)

All hashes in provenance.json, raw evidence SHA256 preserved, registry isolation, TRAIN/TEST split compliance auditable.
