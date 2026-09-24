# EXP-FRONTIER-35937602723 preregistration

**Lane:** frontier — REOPEN C-SEMANTIC-RESOLVE per Global Research Director mandate (parent_handoff SUPERSEDE, cognitive_reset true)
**Experiment ID:** EXP-FRONTIER-35937602723
**Claim:** C-SEMANTIC-RESOLVE — Goals can be resolved to applicable mechanisms without internal ids
**Director mandate source:** `research/experiments/EXP-FRONTIER-35937602723/request.json:director_mandate` — synthetic gate before authorizing live heterogeneous BrowserGym 1280x720 CDP AX>10 WebArena-Verified v2/WebGym 300k shootout targeting O(1) amortized $0.002-0.092 at f=10/100 vs O(MxN) browsing
**Parent handoff:** `research/experiments/EXP-FRONTIER-35921359961/handoff.json` sha 1f7975fc — 15th frontier C-SEMANTIC-RESOLVE alias shootout MEASUREMENT_INVALID at synthetic bounded 20/40=0.50 ceiling (per-family header 10/10 body 10/10 auth 0/10 mixed 0/10 ECE 0.22-0.26, joint 40/40 synthetic selection_log=[] complementary_frac=0.0, |rho| 0.23 p=0.176). Preserved as continuity evidence only per SUPERSEDE; not an authorization for another live shootout until synthetic gate passes.
**Freeze policy:** This prereg + spec.json frozen via deterministic `freeze.json` before any outcome-bearing measurement. Any analysis change after seeing outcomes is exploratory.

---

## 1. Question (Director-refined minimal discriminating test)

Without requiring live BrowserGym 1280x720 CDP Accessibility.getFullAXTree (>10 heterogeneous WebArena-Verified v2/WebGym 300k sample), does synthetic alias variant->canonical catalog + server routing normalization with Fetch/WebMCP OpenAPI discovery (HATEOAS link following + path template normalization regex `${slot}` + Jaccard>=0.6 agglomerative clustering over method/path/header/body/auth_scope) plus joint multi-candidate correct-family composition (2-3 complementary candidates, no cross-family key adoption, softmax temp 0.15 + deterministic jitter gated UNKNOWN<0.80, verify+freshness gates) rescue the bounded single-candidate correct-family ceiling 20/40=0.50 (per-family header 10/10 body 10/10 auth 0/10 mixed 0/10) to pooled >=0.60 (24/40) with gap>=0.10 bootstrap lower>0.05, per-family header>=4/10 mixed>=4/10, false_accept<=0.15 UNKNOWN precision>=0.85 ECE<=0.15 bootstrap upper<=0.18, under frozen honest sum-counter cost (no jitter/n*3200/f*6.0, |rho_shuffled|<0.20 within-f std>0, trajectory-grouped CIs), versus hierarchical xMemory vs flat TFIDF-K5 vs genuine endpoint-catalog single-candidate baselines — establishing synthetic gate before authorizing live heterogeneous shootout?

## 2. Hypothesis

H1 (primary): Joint complementary composition (2-3 candidates whose union covers header+body+query+auth families; per-candidate still forbidden cross-family single adoption) built on a synthetic alias catalog + routing normalization (OpenAPI spec fetch 200 OK with parsed paths/components + HATEOAS + regex `${slot}` normalization + Jaccard>=0.6 clustering) will lift pooled correct-family coverage from the bounded 20/40=0.50 (Wilson [0.352,0.648], McNemar p=1.0 vs flat/hierarchical/catalog as in EXP-FRONTIER-35921359961) to >=0.60 with gain>=0.10 over the best single-candidate baseline (flat TFIDF-K5-CF, hierarchical xMemory-CF, endpoint-catalog-CF), with per-family header>=4/10 and mixed triple-channel header+body+query+auth >=4/10 (jointly correct), false_accept<=0.15 UNKNOWN precision>=0.85 ECE<=0.15 bootstrap upper<=0.18, under honest sum-counter cost |rho_shuffled|<0.20.

H0 (bounded falsification): Even with genuine Jaccard>=0.6 catalogs and verified routing normalization and honest cost, joint composition does not rescue mixed 0/10 to >=4/10 nor raise pooled to >=0.60 with significant gain; single-candidate ceilings 20/40=0.50 are genuine factorization limits for these orthogonal families on the synthetic fixture, not implementation artifacts.

## 3. State representation (frozen)

- **Synthetic-only substrate:** 40 tasks from fixture sha `83b7c52dd17848fc8c70d1c629b8d541788e0438249623ea783d2df364467319` (orthogonal header 10, body 10, auth 10, mixed 10 triple/quad-channel header+body+query+auth). No live BrowserGym 1280x720 CDP required; `live_available` may be false correctly disclosed as synthetic gate not MEASUREMENT_INVALID. Synthetic-to-live gap remains dominant unknown explicitly bounded to fixture.
- **Observation `derived_context` allowed keys only:** `url/method/url_path/url_query/url_segments/headers_observed/body_observed` plus synthetic OpenAPI spec path templates and HATEOAS hrefs via mocked Fetch/WebMCP. **Forbidden keys (oracle leak):** `alias_family/query_key/target_prefix/routing_prefix/target_style/path_style/header_key/body_field/auth_scope/expected_template/expected_endpoint` — any read by alias/endpoint/hierarchical builders triggers NC-ORACLE-LEAK MEASUREMENT_INVALID. Catalogs fit train only; correct-family eligibility derived from parsed template family vs observed canonical family never hidden_expected.
- **Representation loss disclosed:** Variant casing preserved only as canonical; visual pixels/timing/auth token values beyond key presence bounded to tested families; synthetic derived_context may be observationally saturated (expected bound verbatim) due to bound-then-parse fixture design — disclosed but does not invalidate mechanism leverage isolation.
- **Holdout:** Alias forms and mixed compositions stratified; train never sees test alias form nor mixed joint composition. Alias catalog / endpoint catalog / hierarchical centroids fit train only. No site identity leakage.

## 4. Action / catalog representation (frozen)

- Mechanism template string with `${slot}` placeholders in URL/path/query/header/body/auth_scope (mixed 4-channel simultaneously).
- **Alias catalog:** variant->canonical mapping built from train registry variant inventory only, regex `${slot}` normalization, logged size/families.
- **Endpoint catalog (genuine):** regex `${slot}` path templating + Jaccard>=0.6 agglomerative clustering over method/path/header/body/auth_scope TFIDF mean per centroid, centroid count >=6, families covering header/body/query/auth, spec enum extraction if synthetic spec covers path.
- **Hierarchical xMemory:** L1 episodes=mechanisms, L2 components via regex parsing, L3 themes Jaccard>=0.6 agglomerative centroid TFIDF mean, top-down complementary selection entropy>0.4 adaptive k 3-5.
- **Single-candidate pipelines** (FLAT, HIER, ENDPOINT-CATALOG, EXACT) use frozen single-adoption correct-family-required rewriting (alphabetically first eligible, cross-family forbidden). **Joint pipeline** uses complementary set-cover 2-3 candidates jointly covering families (per-candidate still forbidden but union allowed if covers observed families). Confidence via softmax temp 0.15 + deterministic jitter seeded via hashlib.sha256(task_id), gated UNKNOWN<0.80.

## 5. Target

Primary target = `correct_resolution` under correct-family rule per task:
- Retrieved/catalog/joint set contains candidate(s) whose family(ies) match observed canonical family(ies) and after `_bind+verify` yields `expected_bound` (mixed requires all 4 channels jointly correct).
- `false_accept` = wrong binding or should abstain but accepted.
- `UNKNOWN` = gated confidence<0.80 or no applicable mechanism.
- Pooled coverage = mean correct_resolution over 40 synthetic tasks.
- Also report per-family correctness (header/body/auth/mixed each 10), UNKNOWN precision, ECE 5-bin, false_accept, coverage gain, honest cost.

## 6. Sampling policy

- **Synthetic pooled 40** orthogonal fixture (10 per family) primary, plus `exact 12` verbatim intent, `no-applicable 12` OOD without covering mechanism, `empty 6` empty registry => 70 per pipeline for calibration.
- Pipelines 6: `B-EXACT-MATCH-CF, B-FLAT-TFIDF-K5-CF, H-HIERARCHICAL-CF, B-ENDPOINT-CATALOG-CF, B-JOINT-ALIAS-ROUTING-CF (primary), B-RANDOM-K5-CF, B-STAGEHAND isolation` => ~420 synthetic resolve/bind/verify calls, paired per task across pipelines for McNemar.
- Deterministic seeds: `numpy.random.RandomState(42)`, `random.seed(42)`, `hashlib.sha256` for jitter/hashing (never Python `hash()`).
- No live BrowserGym calls; alias/catalog/routing/fetch offline (<15s total).

## 7. Holdout

- Alias families and mixed stratified; test alias forms and mixed joint compositions excluded from alias/endpoint/hierarchical training.
- Alias/endpoint/hierarchical catalogs fit train only; OpenAPI spec enums only from synthetic train spec paths.
- Audit verifies 0/40 registry leak, 0 forbidden-key violations, and single-candidate cross-family adoption ==0 (joint only union coverage).

## 8. Nulls / baselines (frozen, stable IDs)

- **B-EXACT-MATCH-CF** — exact intent equality 0.8, correct-family gating; expects 0/40 alias-OOD, 12/12 exact.
- **B-FLAT-TFIDF-K5-CF** — flat TF-IDF cosine top-k=5, CF single adoption, softmax0.15+jitter.
- **H-HIERARCHICAL-CF** — xMemory L1 episodes L2 components regex L3 themes Jaccard>=0.6.
- **B-ENDPOINT-CATALOG-CF** — genuine Jaccard>=0.6 centroids over method/path/header/body/auth_scope.
- **B-JOINT-ALIAS-ROUTING-CF** — PRIMARY joint: alias catalog + routing normalization (OpenAPI+HATEOAS+`${slot}`) + Jaccard>=0.6 + set-cover 2-3 complementary.
- **B-RANDOM-K5-CF** — chance calibration 0.175.
- **BINDING-RULE** — frozen CF + softmax0.15+jitter UNKNOWN<0.80 + honest sum-counter.

All baselines are strong, code-distinct (manifest hash distinct Jaccard overlap <0.90 between hierarchical/endpoint-catalog/alias-catalog), and necessary to isolate joint leverage from retrieval-diversity tuning (prior 15 sweeps failed to move McNemar p=1.0).

## 9. Primary metric and expected direction

- **Primary metric:** Pooled correct-family coverage on 40 synthetic tasks (B-JOINT minus best single baseline).
- **Expected direction under H1:** Joint pooled >=0.60 (24/40) Wilson lower>0.35 binomial p<0.05 vs 0.10, gain >=0.10 over best single (max flat/hierarchical/endpoint 20/40=0.50), block bootstrap 2000 family-grouped 95% CI lower>0.05 McNemar p<0.05 vs each single baseline, per-family header>=4/10 mixed>=4/10.
- **Secondary calibration/cost gating:** false_accept<=0.15 UNKNOWN precision>=0.85 ECE<=0.15 bootstrap upper<=0.18 |rho_shuffled|<0.20 within-f std>0 not n*3200.
- **Strong null:** Single-candidate flat/hierarchical/endpoint remain at 20/40=0.50 mixed 0/10.

## 10. Uncertainty method

- Wilson 95% CI for proportions (pooled/per-family).
- One-sided binomial vs 0.10 null.
- Paired McNemar (with continuity) per task across pipelines (joint vs each baseline, vs exact).
- Block bootstrap 2000 resamples family-grouped (and synthetic site-equivalent) for coverage gain and ECE CIs.
- Permutation for honest cost: shuffled cost-label correlation |rho_shuffled| with N=200 permutations, reported per pipeline max; requires max<0.20 p>=0.20.
- No Gaussian jitter CI; permutation null only.

## 11. Adequacy rule

Measurement is adequate for confirmatory SURVIVES iff **all** PCs and NCs pass (see spec decision_rule). In particular honest_cost==sum counters diff 0 within-f std>0 |rho|<0.20 for ALL pipelines, catalogs proven genuine Jaccard>=0.6 distinct hash, routing before!=after >=8 pairs logged with task-relevant fraction computed, joint selection_log non-empty complementary_frac>0 (not prior vacuous []), forbidden-key reads 0, registry leak 0/40, harness errors <=20%, confidence std>0.05. Adequacy failure => MEASUREMENT_INVALID regardless of pooled metrics (not a falsification).

## 12. Falsification / survival rule (frozen)

**SURVIVES_CURRENT_TEST** iff adequacy PASS **and** all hold:
1. PC-EXACT-MATCH >=0.90 false<=0.10; PC-ALIAS-CATALOG-BUILT/Jaccard>=0.6 distinct; PC-ENDPOINT-CATALOG centroids>=6; PC-HIERARCHICAL themes>=3; PC-FLAT-HEALTH non-empty>=90%; PC-OPENAPI-SYNTHETIC 200 parsed; PC-ROUTING-DIFF >=8 before!=after; PC-HONEST-COST-SANITY all pipelines |rho|<0.20 within-f std>0 not n*3200; PC-CONFIDENCE-DERIVED std>0.05; PC-FRESHNESS-NONCIRCULAR
2. NC-NO-APPLICABLE precision>=0.85 false<=0.15 all pipelines; NC-EMPTY 100%; NC-ORACLE-LEAK 0; NC-BIJECTIVE-COST not n*3200; NC-STAGEHAND 0/40
3. S1 pooled joint >=0.60 Wilson lower>0.35 binomial p<0.05 McNemar p<0.05 vs exact (0/40) and vs best single baseline
4. S2 coverage >=0.60 gain>=0.10 over best single block bootstrap lower>0.05 p<0.05
5. S3 per-family header>=4/10 mixed>=4/10 (and auth>=4/10 diagnostic)
6. S4 false_accept<=0.15 precision>=0.85
7. S5 ECE<=0.15 bootstrap upper<=0.18
8. S6 honest cost non-bijective joint within 2x baselines modeled amortized within $0.002-0.092 disclosed

**FALSIFIED-IN-SETTING** if adequacy PASS but any S1-S6 fails (joint pooled<0.60 or gain<0.10 NS or mixed<4/10 or false>0.15 or ECE>0.15 etc). Bounded to synthetic fixture only; does NOT close live hetero question.

**MEASUREMENT_INVALID** if any PC/NC fails — infrastructure/harness failure, not scientific falsification; do not interpret as ceiling proof.

**MIXED** if adequacy PASS but pooled 0.525-0.60 or gain 0.05-0.10 or mixed 2-3/10 or ECE 0.15-0.18.

## 13. Validity threats and representation loss

- **Prior ceiling artifact:** Prior 20/40=0.50 Wilson [0.352,0.648] per-family header 10/10 body 10/10 auth 0/10 mixed 0/10 replicated 15 times with McNemar p=1.0 indicates genuine single-candidate CF factorization limit not random noise; joint rescue hypothesis directly tests 0.5^3 compounding vs routing.
- **Synthetic saturation:** Fixture derived_context may contain expected bound verbatim (tautological bound-then-parse); 1.0 would reflect copy via adopt-any-observed-key-not-in-registry (audit V1 medium). We disclose and require joint selection_log>0 complementary_frac>0 to prove genuine exercise, not vacuous  [] as prior.
- **ECE bimodal:** Perfect accuracy on synthetic yields 3 empty ECE bins (reported in prior 0.11-0.24); we still require ECE<=0.15 upper<=0.18 but disclose bimodal limitation; live imperfect accuracy remains dominant unknown.
- **Honest cost fragility:** Prior |rho| 0.23 p=0.176 on hierarchical marginally exceeded 0.20 despite correct harness; we require max across ALL pipelines <0.20 with permutation reporting and within-f std>0 not n*3200 to guarantee no bijective proxy (n*3200, f*6.0 jitter explicitly forbidden).
- **Catalog distinctness:** Prior failures were code-identity (flat/hierarchical/endpoint identical implementations); we require manifest hash distinct overlap<0.90 and Jaccard threshold logged.
- **Routing confound:** Prior PC-ROUTING-DIFF 14/58 synthetic vs task-relevant 6/40=15% <20% live gate; for this synthetic gate we require >=8 before!=after overall with task-relevant fraction disclosed, explicitly not requiring live >=20% task-relevant which is synthetic artifact.
- **Browser invalidity:** This synthetic gate explicitly does NOT require live BrowserGym; MEASUREMENT_INVALID only if harness itself fails, not if live unavailable.
- **Strong baselines:** Comparison is against strongest single-candidate baselines including genuine Jaccard>=0.6 endpoint catalog, not weak no-memory.

## 14. Product consequences

- **If SURVIVES:** Synthetic alias catalog + routing normalization + joint 2-3 composition isolates mechanism leverage from live substrate and beats all single-candidate retrieval-diversity baselines; authorizes immediate live heterogeneous BrowserGym 1280x720 CDP AX>10 shootout with genuine spec coverage >=70% and routing >=20% task-relevant, targeting O(1) $0.002-0.092 at f=10/100 vs O(MxN) browsing with measured tokens/latency. C-SEMANTIC-RESOLVE advances to EXPERIMENTAL synthetic-gate-passed (not VALIDATED/PRODUCT_CORE). Frontier should prioritize Fetch/WebMCP + joint architecture.
- **If FALSIFIED-IN-SETTING:** Even genuine alias/routing/joint fails to rescue synthetic ceiling under honest cost; product must NOT add alias catalog/routing/joint layer as higher-leverage vs flat/hierarchical/endpoint for these families; keep flat RAG or exact and pivot frontier to orthogonal basins (residual-novelty barrier-physics/rewind memory, verification economics, per-value alias handling via runtime/intel) rather than 16th alias sweep. Bounded ceiling 21/40=0.525 preserved as genuine correct-family limit.
- **If MEASUREMENT_INVALID:** Fix harness (Jaccard proof, routing log, joint non-vacuous, honest cost |rho|<0.20, derived confidence, no leak) and re-run synthetic gate before any live authorization; do not interpret as falsification.

## 15. Estimated cost and information gain

- **Cost:** Low CPU-only: ~420 synthetic calls + alias/catalog/routing/fetch offline <15s; no BrowserGym install; TFIDF <2s; no LLM tokens; wall-clock <15 min; <500 MB tmp.
- **Gain:** Very high per cost as Director-mandated minimal discriminating gate: 15 prior MEASUREMENT_INVALID live-heavy shootouts (same 0.50-0.525 ceiling) have near-zero marginal information vs testing orthogonal joint composition class outside retrieval-diversity basin. This <15 min synthetic gate either authorizes live O(1) economics shootout or cleanly parks alias/routing/joint for these families, changing next allocation per portfolio 309-exp tunnel diagnosis (80 invalid, 0 product_core). Cognitive reset per REOPEN charter.

## 16. Preregistration integrity

No outcome-bearing measurements were run during DESIGN. All seeds, thresholds, and controls frozen per spec.json. Any deviation after freeze is exploratory and labeled as such. EXECUTE must not mutate frozen inputs; AUDIT must use stable metric/control IDs; DIRECTOR integrates only surviving evidence per research/EXPERIMENT_PACKET.md.

