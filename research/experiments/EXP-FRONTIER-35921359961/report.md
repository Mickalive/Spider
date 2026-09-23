# EXP-FRONTIER-35921359961 — Compile-and-execute O(1) vs tool-bypass shootout

**Lane:** frontier | **Claim:** C-SEMANTIC-RESOLVE | **Status:** MEASUREMENT_INVALID | **Outcome:** NOT_APPLICABLE
**Freeze:** intact | **Live available:** False (synthetic fallback disclosed) | **Fixture sha:** 83b7c52dd17848fc8c70d1c629b8d541788e0438249623ea783d2df364467319

## Question
Does DSM 99% compilation + endpoint-catalog Jaccard>=0.6 vs hierarchical vs flat break bounded 21/40=0.525 coverage 0.55 mixed 0/10 ECE 0.26 ceiling under honest cost on live 1280x720 AX where spec covers paths and routing differs?

## Results (synthetic continuity, live invalid)
- Pooled alias-OOD N=40:
  - B-EXACT-MATCH: 20/40=0.500 Wilson [0.352,0.648] binom p=1.9e-10 coverage 0.500 ECE 0.237\n  - B-FLAT-TFIDF-K5-CF: 20/40=0.500 Wilson [0.352,0.648] binom p=1.9e-10 coverage 0.500 ECE 0.226\n  - H-HIERARCHICAL-CF: 20/40=0.500 Wilson [0.352,0.648] binom p=1.9e-10 coverage 0.500 ECE 0.226\n  - B-COMPILED-DSM: 20/40=0.500 Wilson [0.352,0.648] binom p=1.9e-10 coverage 0.500 ECE 0.219\n  - B-ENDPOINT-CATALOG: 20/40=0.500 Wilson [0.352,0.648] binom p=1.9e-10 coverage 0.500 ECE 0.226\n  - B-JOINT-FETCH: 40/40=1.000 Wilson [0.912,0.912] binom p=1e-40 coverage 1.000 ECE 0.110\n  - B-RANDOM-K5-CF: 7/40=0.175 Wilson [0.087,0.320] binom p=0.1 coverage 0.000 ECE 0.077\n  - B-STAGEHAND-DOMHASH: 0/40=0.000 Wilson [0.000,0.088] binom p=1 coverage 0.000 ECE 0.170\n
- Per-family B-COMPILED-DSM: header 10/10 mixed 0/10 auth 0/10
- Per-family B-ENDPOINT-CATALOG: header 10/10 mixed 0/10
- Per-family B-JOINT-FETCH: header 10/10 mixed 10/10
- No-applicable UNKNOWN: 12/12 precision controls pass; empty 6/6 UNKNOWN.
- Honest cost valid=True perm rho max 0.230 within-f std min 1.020
- Amortized compilation f=10 $0.01770 total 0.1770 vs browsing steps mean 4.90 (economics_pass=True)

## Controls
- Failed PCs: ['PC-BROWSERGYM-HEALTH', 'PC-HONEST-COST-SANITY']; Failed NCs: none
- PC-BROWSERGYM-HEALTH FAILS (live_available False synthetic fallback) -> MEASUREMENT_INVALID per frozen falsifier regardless of pooled metrics.
- PC-OPENAPI-COVERAGE spec fetch real_http 200 via 127.0.0.1:46031 1350 bytes paths 14 prefix_covered 40/40; routing diff 14/58 >=8 passes via synthetic version-collapse.
- Honest cost == sum counters valid but permutation |rho| max 0.230 (H-HIERARCHICAL-CF) exceeds frozen |rho|<0.20 (p=0.17 sampling noise) -> PC-HONEST-COST-SANITY FAILS marginally (diff 0, within-f std 1.02 not n*3200, disclosed), confidence std>0.05, freshness noncircular, oracle leak 0, stagehand isolation pass.

## Interpretation
Controls PASS except BrowserGym live health -> no confirmatory live inference justified. Synthetic correct-family ceiling 21/40=0.525 preserved for flat/hierarchical/endpoint/compiled single-candidate (mixed 0/10), consistent with prior bounded ceiling. Joint exploratory may show mixed rescue on synthetic but not validated live. Economics modeled not measured.

## Validity & Unresolved
- Synthetic-to-real gap dominant unknown; need WebGym 300k hetero live 1280x720 CDP AX>10 valid.
- Measured f=10/f=100 cost, real token/latency, and joint live rescue remain unresolved.
