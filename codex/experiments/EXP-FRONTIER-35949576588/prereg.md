# EXP-FRONTIER-35949576588 preregistration

**Lane:** frontier — CONTINUE C-SEMANTIC-RESOLVE per Global Research Director mandate (cognitive_reset true)
**Experiment ID:** EXP-FRONTIER-35949576588
**Claim:** C-SEMANTIC-RESOLVE — Goals can be resolved to applicable mechanisms without internal ids
**Director mandate source:** `research/experiments/EXP-FRONTIER-35949576588/request.json:director_mandate` — synthetic gate before authorizing live heterogeneous BrowserGym 1280x720 CDP AX>10 WebArena-Verified v2/WebGym 300k shootout targeting O(1) amortized $0.002-0.092 at f=10/100 vs O(MxN) browsing
**Parent handoff:** `research/experiments/EXP-FRONTIER-35937602723/handoff.json` sha f05142997ed7de42bcab01b8e9528bacf1f3951972ca07e07db6a173f14d6ee2 — 16th frontier C-SEMANTIC-RESOLVE synthetic shootout 40/40=1.0 pooled vs 20/40=0.50 singles but audit REVISE: degenerate 13-singleton alias catalog min Jaccard 0.0, value-only bounds_equal inflates B-EXACT 20/40 vs expected 0/40, routing 10/55 not causal, Fetch spec unused, honest rho 0.0 degenerate, verbatim saturation tautology. Preserved as continuity evidence only per director_mandate parent_handoff_disposition USE; not an authorization for another live shootout until repaired synthetic gate passes. Established/rejected/unknown/do_not_assume distinctions preserved below.
**Freeze policy:** This prereg + spec.json frozen via deterministic `freeze.json` before any outcome-bearing measurement. Any analysis change after seeing outcomes is exploratory.

---

## 1. Question (Director-refined minimal discriminating test)

Without requiring live BrowserGym 1280x720 CDP Accessibility.getFullAXTree (>10 heterogeneous WebArena-Verified v2/WebGym 300k sample), does synthetic alias variant->canonical catalog + server routing normalization with Fetch/WebMCP OpenAPI discovery (HATEOAS link following + OpenAPI spec fetch + path template normalization regex `${slot}` + Jaccard>=0.6 agglomerative clustering over method/path/header/body/auth_scope) plus joint multi-candidate correct-family composition (2-3 complementary candidates, no cross-family key adoption verified by exact expected key-set equality not value-only bounds_equal, genuine multi-variant alias classes >=2 variants/class merged at Jaccard>=0.6 min_pairwise>=0.6, softmax temp 0.15+jitter UNKNOWN<0.80 verify+freshness gates) rescue the bounded single-candidate correct-family ceiling 21/40=0.525 (per-family header 10/10 body 10/10 auth 0/10 mixed 0/10 value-only inflated, expected 0-5/40 key-sensitive) to pooled >=0.60 (24/40) with gain>=0.10 bootstrap lower>0.05, per-family header>=4/10 mixed>=4/10 key-sensitive, with ablation causality joint-with >=4/10 mixed vs joint-without alias <=3/10 and joint-without routing <=3/10, false_accept<=0.15 UNKNOWN precision>=0.85 ECE<=0.15 bootstrap upper<=0.18, under frozen honest sum-counter cost (sum resolve+bind+verify+freshness+browser_steps+alias/catalog/fetch/spec/joint counters, no jitter/n*3200/f*6.0, |rho_shuffled|<0.20 within-f std>0, trajectory-grouped CIs 2000), versus hierarchical xMemory decoupling, flat TFIDF-K5, and genuine endpoint-catalog single-candidate baselines — establishing synthetic gate before authorizing live heterogeneous shootout for O(1) economics, and if not, pivot basin per handoff?

## 2. Hypothesis

H1 (primary): Joint complementary composition (adaptive 2-3 candidates whose union of canonical key-sets equals expected key-set; per-candidate still forbidden cross-family key adoption, verified by exact expected key-set equality after alias resolution and routing normalization, not value-only bounds_equal) built on a genuine synthetic alias catalog (each alias family >=2 variants merged at Jaccard>=0.6 min_pairwise>=0.6, catalog built train-only via regex `${slot}` normalization) + server routing normalization (OpenAPI path template table + regex `${slot}` version-collapse/trailing-slash/case) + Fetch/WebMCP OpenAPI discovery (spec fetch 200 OK parsed paths/components + HATEOAS) will lift pooled correct-family key-sensitive coverage from the bounded 21/40=0.525 (and 0-5/40 under strict key check) to >=0.60 with gain>=0.10 over best single baseline (flat TFIDF-K5-CF, hierarchical xMemory-CF, endpoint-catalog-CF) and over each ablated joint (without alias, without routing, without both), with per-family header>=4/10 and mixed triple-channel header+body+query+auth >=4/10 jointly correct key-sets, false_accept<=0.15 UNKNOWN precision>=0.85 ECE<=0.15 bootstrap upper<=0.18, honest sum-counter |rho_shuffled|<0.20 trajectory-grouped.

H0 (bounded falsification): Even with genuine Jaccard>=0.6 multi-variant catalog, verified routing normalization, honest cost, and Fetch/WebMCP, joint composition does not rescue mixed 0/10 to >=4/10 nor raise pooled to >=0.60 with significant gain over best single and over ablations; single-candidate ceilings are genuine factorization limits for these orthogonal families on repaired synthetic fixture, not implementation artifacts; verbatim saturation via adoption_value_template explains prior 40/40.

## 3. State representation (frozen)

- **Synthetic-only substrate:** 40 tasks from repaired synthetic orthogonal fixture derived from sha `83b7c52dd17848fc8c70d1c629b8d541788e0438249623ea783d2df364467319` but **repaired** to satisfy: each alias family (header, body, query, auth) has >=2 variants with pairwise Jaccard>=0.6 min_pairwise>=0.6, and at least 2 mixed tasks require routing normalization (path versioned/trailing-slash). Prior 13 singleton catalog min Jaccard 0.0 is REJECTED. Orthogonal families header 10, body 10, auth 10, mixed 10 triple/quad-channel header+body+query+auth. No live BrowserGym 1280x720 CDP required; `live_available` may be false correctly disclosed as synthetic gate not MEASUREMENT_INVALID. Synthetic-to-live gap remains dominant unknown explicitly bounded to fixture.
- **Observation `derived_context` allowed keys only:** `url/method/url_path/url_query/url_segments/headers_observed/body_observed` plus synthetic OpenAPI spec path templates and HATEOAS hrefs via mocked Fetch/WebMCP. **Forbidden keys (oracle leak):** `alias_family/query_key/target_prefix/routing_prefix/target_style/path_style/header_key/body_field/auth_scope/expected_template/expected_endpoint` — any read by alias/endpoint/hierarchical builders triggers NC-ORACLE-LEAK MEASUREMENT_INVALID. Catalogs fit train only; correct-family eligibility derived from parsed template family vs observed canonical family key-sets, never hidden_expected.
- **Key-sensitive verification (repair):** Correctness now requires exact expected key-set equality (sorted canonical keys after alias resolution and routing normalization) plus value equality, not value-only bounds_equal. Audit `required_fixes[2]` mandates this; code must implement `normalize_bound_key_sensitive`. Value-only correctness that made alias handling vacuous is REJECTED (handoff rejected #4).
- **Representation loss disclosed:** Variant casing canonicalized only; visual pixels/timing/auth token values beyond key presence bounded to tested families; synthetic derived_context may be observationally saturated (expected bound verbatim) but ablations (JOINT-NO-ALIAS, JOINT-NO-ROUTING, JOINT-NO-BOTH) isolate generic verbatim copy from alias/routing factorization.
- **Holdout:** Alias forms and mixed compositions stratified; train never sees test alias form nor mixed joint composition. Alias catalog / endpoint catalog / hierarchical centroids fit train only. No site identity leakage.

## 4. Action / catalog representation (frozen)

- Mechanism template string with `${slot}` placeholders in URL/path/query/header/body/auth_scope (mixed 4-channel simultaneously).
- **Alias catalog (genuine):** variant->canonical mapping built from train registry variant inventory only, regex `${slot}` normalization, Jaccard>=0.6 agglomerative merging per family, each family >=2 variants, min_pairwise>=0.6 verified, logged size/families/pairwise matrix. Prior singleton identity mapping is REJECTED.
- **Endpoint catalog (genuine):** regex `${slot}` path templating + Jaccard>=0.6 agglomerative clustering over method/path/header/body/auth_scope TFIDF mean per centroid, centroid count >=6, families covering header/body/query/auth, spec enum extraction if synthetic spec covers path.
- **Hierarchical xMemory:** L1 episodes=mechanisms, L2 components via regex parsing, L3 themes Jaccard>=0.6 agglomerative centroid TFIDF mean, top-down complementary selection entropy>0.4 adaptive k 3-5.
- **Single-candidate pipelines** (FLAT, HIER, ENDPOINT-CATALOG, EXACT) use frozen single-adoption correct-family-required rewriting (alphabetically first eligible, cross-family forbidden, key-sensitive exact key-set check).
- **Joint pipelines:** `B-JOINT-FULL-CF` uses complementary set-cover 2-3 candidates jointly covering families (per-candidate still forbidden but union key-set must equal expected). `B-JOINT-NO-ALIAS-CF` disables alias lookup (identity only), `B-JOINT-NO-ROUTING-CF` disables routing normalization, `B-JOINT-NO-BOTH-CF` disables both (generic verbatim set-cover). Confidence via softmax temp 0.15 + deterministic jitter seeded via hashlib.sha256(task_id), gated UNKNOWN<0.80. Ablations required to isolate alias vs routing causality per `audit required_fixes[1]`.
- **Fetch/WebMCP:** Mocked ThreadingHTTPServer, fetch_openapi_spec 200 OK 14 paths synthetic, HATEOAS link following >=1, logged in fetch_manifest.json. Prior Fetch unused for scoring is REJECTED; here Fetch path table must feed routing normalization but ablation still isolates.

## 5. Target

Primary target = `correct_resolution` under correct-family **key-sensitive** rule per task:
- Retrieved/catalog/joint set contains candidate(s) whose family(ies) match observed canonical family(ies) and after alias resolution + routing normalization + `_bind+verify` yields **exact expected key-set equality** (sorted canonical keys) AND expected_bound values jointly correct (mixed requires all 4 channels jointly correct key-sets + values).
- `false_accept` = wrong key-set or should abstain but accepted; `UNKNOWN` = gated confidence<0.80 or no applicable mechanism.
- Pooled coverage = mean correct_resolution over 40 synthetic tasks key-sensitive.
- Also report per-family correctness (header/body/auth/mixed each 10 key-sensitive), UNKNOWN precision, ECE 5-bin derived confidence, false_accept, coverage gain vs best single and vs ablations, honest cost, joint selection details.

## 6. Sampling policy

- **Synthetic pooled 40** repaired orthogonal fixture (10 per family) primary, plus `exact 12` verbatim intent key-sensitive, `no-applicable 12` OOD without covering mechanism, `empty 6` empty registry => 70 per pipeline for calibration.
- Pipelines 9-10: `B-EXACT-MATCH-CF, B-FLAT-TFIDF-K5-CF, H-HIERARCHICAL-CF, B-ENDPOINT-CATALOG-CF, B-JOINT-FULL-CF (primary), B-JOINT-NO-ALIAS-CF, B-JOINT-NO-ROUTING-CF, B-JOINT-NO-BOTH-CF, B-RANDOM-K5-CF, B-STAGEHAND isolation` => ~630 synthetic resolve/bind/verify calls, paired per task across pipelines for McNemar.
- Deterministic seeds: `numpy.random.RandomState(42)`, `random.seed(42)`, `hashlib.sha256` for jitter/hashing (never Python `hash()`).
- Honest cost permutation N_PERMS=200 trajectory-grouped; block bootstrap 2000 family-grouped for CIs.
- No live BrowserGym calls; alias/catalog/routing/fetch offline (<15s total) CPU-only.

## 7. Holdout

- Alias families and mixed stratified; test alias forms and mixed joint compositions excluded from alias/endpoint/hierarchical training.
- Alias/endpoint/hierarchical catalogs fit train only; OpenAPI spec enums only from synthetic train spec paths. For genuine alias families, train variants differ from test variants but share Jaccard>=0.6 within family.
- Audit verifies 0/40 registry leak, 0 forbidden-key violations, single-candidate cross-family adoption ==0 (joint only union coverage with exact key-set equality), and ablation disabled flags logged. No site identity leakage.

## 8. Nulls / baselines (frozen, stable IDs)

- **B-EXACT-MATCH-CF** — exact intent equality 0.8, correct-family key-sensitive gating; expects 0/40 alias-OOD, 12/12 exact.
- **B-FLAT-TFIDF-K5-CF** — flat TF-IDF cosine top-k=5, CF single adoption key-sensitive, softmax0.15+jitter.
- **H-HIERARCHICAL-CF** — xMemory L1 episodes L2 components regex L3 themes Jaccard>=0.6 key-sensitive.
- **B-ENDPOINT-CATALOG-CF** — genuine Jaccard>=0.6 centroids over method/path/header/body/auth_scope key-sensitive.
- **B-JOINT-FULL-CF** — PRIMARY joint: genuine alias catalog min_pairwise>=0.6 + routing + Fetch/HATEOAS + Jaccard>=0.6 + set-cover 2-3 complementary key-sensitive.
- **B-JOINT-NO-ALIAS-CF** — ablation without alias lookup (routing+joint only).
- **B-JOINT-NO-ROUTING-CF** — ablation without routing normalization (alias+joint only).
- **B-JOINT-NO-BOTH-CF** — ablation without alias and routing (verbatim set-cover only).
- **B-RANDOM-K5-CF** — chance calibration.
- **BINDING-RULE** — frozen CF key-sensitive + softmax0.15+jitter UNKNOWN<0.80 + honest sum-counter key-sensitive.

All baselines strong, code-distinct (manifest hash distinct Jaccard overlap <0.90 between hierarchical/endpoint-catalog/alias-catalog), necessary to isolate joint alias+routing leverage from retrieval-diversity tuning (prior 16 sweeps McNemar p=1.0) and from verbatim saturation.

## 9. Primary metric and expected direction

- **Primary metric:** Pooled correct-family key-sensitive coverage on 40 synthetic tasks (B-JOINT-FULL vs best single baseline AND vs ablations).
- **Expected direction under H1:** Joint-FULL pooled >=0.60 (24/40) Wilson lower>0.35 binomial p<0.05 vs 0.10, gain >=0.10 over best single (max flat/hierarchical/endpoint expected 0-5/40 key-sensitive, reference 21/40=0.525 value-only) with block bootstrap 2000 trajectory-grouped 95% CI lower>0.05 McNemar p<0.05 vs each single baseline, **and** gain >=0.10 vs each ablation (NO-ALIAS, NO-ROUTING, NO-BOTH) with bootstrap lower>0.05, per-family header>=4/10 mixed>=4/10 key-sensitive with ablations <=3/10 mixed.
- **Secondary gating:** false_accept<=0.15 UNKNOWN precision>=0.85 ECE<=0.15 bootstrap upper<=0.18 |rho_shuffled|<0.20 within-f std>0 not n*3200.
- **Strong null:** Single-candidate flat/hierarchical/endpoint and ablated joints remain at <=3/10 mixed and pooled ~0.05-0.125.

## 10. Uncertainty method

- Wilson 95% CI for proportions (pooled/per-family key-sensitive).
- One-sided binomial vs 0.10 null.
- Paired McNemar (with continuity) per task across pipelines (joint-FULL vs each baseline, vs exact, vs each ablation).
- Block bootstrap 2000 resamples trajectory-grouped by family (and synthetic site-equivalent) for coverage gain (vs best single and vs ablations) and ECE CIs.
- Permutation for honest cost: shuffled cost-label correlation |rho_shuffled| with N=200 permutations per pipeline, trajectory-grouped, reported per pipeline max; requires max<0.20 p>=0.20 for non-constant pipelines; constant-outcome pipelines report N/A with disclosure (prior joint rho 0.0 degenerate REJECTED).
- No Gaussian jitter CI; permutation null only; ECE bootstrap trajectory-grouped.
- All CIs family-grouped not iid.

## 11. Adequacy rule

Measurement adequate for confirmatory SURVIVES iff **all** PCs and NCs pass (see spec decision_rule). In particular: alias catalog genuine min_pairwise>=0.6 each family >=2 variants (not parent 13 singleton 0.0), routing before!=after >=8 pairs logged, Fetch spec 200 parsed, joint selection_log non-empty complementary_frac>0 k in {2,3} (not prior vacuous []), key-sensitive exact key-set equality enforced (audit code check not value-only), honest_cost==sum counters diff 0 within-f std>0 per non-constant pipeline |rho|<0.20 trajectory-grouped N_PERMS=200 (constant reports N/A), derived confidence std>0.05, forbidden-key reads 0, registry leak 0/40, harness errors <=20%, ablation logs non-degenerate. Adequacy failure => MEASUREMENT_INVALID regardless of pooled metrics (not falsification).

## 12. Falsification / survival rule (frozen)

**SURVIVES_CURRENT_TEST** iff adequacy PASS **and** all hold:
1. All PCs PASS (PC-EXACT-MATCH >=0.90 false<=0.10 key-sensitive; PC-ALIAS-CATALOG-GENUINE min_pairwise>=0.6 each family >=2 variants distinct overlap<0.90; PC-ENDPOINT-CATALOG centroids>=6; PC-HIERARCHICAL themes>=3; PC-FLAT-HEALTH >=90%/50%; PC-OPENAPI-SYNTHETIC 200 parsed; PC-ROUTING-DIFF >=8 before!=after; PC-KEY-SENSITIVE-VERIFICATION enforced; PC-HONEST-COST-SANITY all non-constant |rho|<0.20 within-f std>0 not n*3200; PC-CONFIDENCE-DERIVED std>0.05; PC-FRESHNESS-NONCIRCULAR)
2. All NCs PASS (NC-NO-APPLICABLE precision>=0.85 false<=0.15 key-sensitive all pipelines; NC-EMPTY 100%; NC-ORACLE-LEAK 0; NC-BIJECTIVE-COST not n*3200; NC-STAGEHAND 0/40; NC-ABLATION-NONDEGENERATE)
3. S1 pooled joint-FULL >=0.60 Wilson lower>0.35 binomial p<0.05 McNemar p<0.05 vs exact (0/40) and vs best single baseline
4. S2 coverage gain>=0.10 over best single block bootstrap lower>0.05 p<0.05 AND gain>=0.10 over each ablation (NO-ALIAS, NO-ROUTING, NO-BOTH) bootstrap lower>0.05
5. S3 per-family header>=4/10 mixed>=4/10 key-sensitive (and auth>=4/10 diagnostic); ablation causality: JOINT-FULL mixed >=4/10 AND JOINT-NO-ALIAS mixed <=3/10 AND JOINT-NO-ROUTING mixed <=3/10 AND JOINT-NO-BOTH mixed <=3/10 (if routing neutral on header/body families, at least NO-ALIAS and NO-BOTH <=3/10 with disclosure)
6. S4 false_accept<=0.15 precision>=0.85 for JOINT-FULL
7. S5 ECE<=0.15 bootstrap upper<=0.18 for JOINT-FULL (key-sensitive imperfect accuracy ensures bins filled)
8. S6 honest cost non-bijective joint within 2x baselines modeled amortized within $0.002-0.092 disclosed

**FALSIFIED-IN-SETTING** if adequacy PASS but any S1-S6 fails (joint pooled<0.60 or gain<0.10 NS vs best single or vs ablations or mixed<4/10 or ablation delta fails: NO-ALIAS >3/10 or NO-ROUTING >3/10 showing rescue not isolated to alias+routing, or false>0.15 ECE>0.15 etc). Bounded to repaired synthetic fixture only; does NOT close live heterogeneous question.

**MEASUREMENT_INVALID** if any PC/NC fails — infrastructure/harness failure, not scientific falsification; do not interpret as ceiling proof. Includes key-sensitive not enforced, degenerate alias catalog, routing not proven, constant rho degenerate not N/A, verbatim saturation without ablation control.

**MIXED** if adequacy PASS but pooled 0.525-0.60 or gain 0.05-0.10 or mixed 2-3/10 or ECE 0.15-0.18 with disclosure.

## 13. Validity threats and representation loss

- **Prior ceiling inflated:** Prior 20/40=0.50 Wilson [0.352,0.648] per-family header 10/10 body 10/10 auth 0/10 mixed 0/10 under value-only bounds_equal inflated B-EXACT to 20/40 vs expected 0/40 alias-OOD. **Repair:** key-sensitive exact key-set equality now required; singles expected 0-5/40. Failure to enforce is PC-KEY-SENSITIVE-VERIFICATION MEASUREMENT_INVALID.
- **Degenerate alias catalog:** Parent 13 singleton classes min Jaccard 0.0 never tested Jaccard>=0.6 clustering, catalog is identity variant->self. **Repair:** Require genuine multi-variant classes >=2 variants/class min_pairwise>=0.6; PC-ALIAS-CATALOG-GENUINE fails if not met. Do not assume Jaccard>=0.6 was exercised (do_not_assume #2).
- **Routing not causal:** Prior PC-ROUTING-DIFF 10/55 synthetic vs task-relevant 6/40=15% <20% live gate, and no task required routing to succeed. **Repair:** Require >=8 before!=after pairs logged and at least 2 mixed tasks require routing; ablation NO-ROUTING tests causality. Do not assume 10/55 proves Director live gate (do_not_assume #3).
- **Fetch unused:** Joint fetched spec but return unused for scoring (audit validity). **Repair:** Fetch path table must feed routing normalization and be logged; ablation still isolates Fetch contribution via NO-BOTH. Do not assume Fetch contributed (do_not_assume #5).
- **Synthetic saturation verbatim copy:** Fixture derived_context may contain expected bound verbatim allowing trivial copy via adopt_any_observed_key_not_in_registry (audit). Prior joint 40/40 with complementary_frac_mean 1.0 but selection_log complementary may still be verbatim copy. **Repair:** Ablations JOINT-NO-ALIAS/NO-ROUTING/NO-BOTH test whether rescue is generic set-cover verbatim vs alias/routing factorization; if ablations also >=4/10, rescue is not alias/routing-specific (FALSIFIED).
- **Honest cost degenerate:** Prior joint rho 0.0 p=1.0 degenerate because correctness constant 40/40 makes Spearman NaN->0. **Repair:** Require outcome variance >0 (fixture designed imperfect accuracy) or report N/A not 0.0; require within-f std>0 per pipeline, |rho|<0.20 trajectory-grouped N_PERMS=200. Do not assume |rho| 0.0 validates joint (do_not_assume #6).
- **ECE bimodal trivial:** Prior perfect 40/40 empties 3 ECE bins trivially calibrates 0.0895. **Repair:** Key-sensitive imperfect accuracy yields filled bins; still require ECE<=0.15 upper<=0.18 with bootstrap. Do not assume 0.0895 transfers to live (do_not_assume #7).
- **Catalog distinctness:** Prior failures were code-identity flat/hierarchical/endpoint identical implementations. Require manifest hash distinct overlap<0.90 and Jaccard threshold logged.
- **C-SEMANTIC-RESOLVE not VALIDATED:** Remains EXPERIMENTAL synthetic ceiling, audit REVISE not PASS, no live replication. No promotion without live heterogeneous BrowserGym 1280x720 CDP AX>10 and f=100 Pareto.
- **Strong baselines:** Comparison is against strongest single-candidate baselines including genuine Jaccard>=0.6 endpoint catalog and ablated joints, not weak no-memory.

## 14. Product consequences

- **If SURVIVES:** Synthetic alias catalog with genuine Jaccard>=0.6 multi-variant classes + routing normalization + joint 2-3 composition isolates mechanism leverage from live substrate and beats all single-candidate retrieval-diversity baselines AND beats ablated joints, proving alias+routing factorization causal. Authorizes immediate live heterogeneous BrowserGym 1280x720 CDP AX>10 shootout with genuine spec coverage >=70% and routing >=20% task-relevant, targeting O(1) $0.002-0.092 at f=10/100 vs O(MxN) browsing with measured tokens/latency/browser work. C-SEMANTIC-RESOLVE advances to EXPERIMENTAL synthetic-gate-passed (not VALIDATED/PRODUCT_CORE). Frontier should prioritize Fetch/WebMCP + joint architecture with genuine alias clustering.
- **If FALSIFIED-IN-SETTING:** Even genuine alias/routing/joint fails to rescue synthetic ceiling under honest cost and key-sensitive verification, or ablation delta fails (generic set-cover explains rescue). Product must NOT add alias catalog/routing/joint layer as higher-leverage vs flat/hierarchical/endpoint for these families; keep flat RAG or exact and pivot frontier to orthogonal basins (residual-novelty verification economics with UNKNOWN precision>=0.85, barrier-physics rewind memory, per-value alias handling via runtime/intel) rather than 17th alias sweep. Bounded ceiling 21/40=0.525 preserved as genuine correct-family key-sensitive limit. Park alias/routing/joint for these families per handoff.
- **If MEASUREMENT_INVALID:** Fix harness (Jaccard proof min_pairwise>=0.6 genuine classes, routing before!=after >=8, spec fetch logged, joint non-vacuous, honest cost |rho|<0.20, derived confidence, key-sensitive verification, no leak, ablations non-degenerate) and re-run synthetic gate before any live authorization; do not interpret as falsification.

## 15. Estimated cost and information gain

- **Cost:** Low CPU-only: ~630 synthetic calls + alias/catalog/routing/fetch offline <15s; no BrowserGym install; TFIDF <2s; no LLM tokens; wall-clock <15 min; <500 MB tmp; <$1 compute.
- **Gain:** Very high per cost as Director-mandated minimal discriminating gate with cognitive reset: 16 prior MEASUREMENT_INVALID alias-OOD sweeps have near-zero marginal VOI; this <15 min repaired synthetic gate with key-sensitive verification, genuine Jaccard>=0.6, and ablated delta either authorizes live O(1) economics shootout or cleanly parks alias/routing/joint for these families at bounded ceiling, changing next allocation per portfolio 319-exp tunnel diagnosis and handoff why_next. Addresses highest-EV gate before live heterogeneous shot.

## 16. Preregistration integrity

No outcome-bearing measurements were run during DESIGN. All seeds, thresholds, controls, and ablation deltas frozen per spec.json. Any deviation after freeze is exploratory and labeled as such. EXECUTE must not mutate frozen inputs; must implement key-sensitive exact key-set equality, genuine alias construction, honest sum-counter with trajectory-grouped 2000 bootstrap and N_PERMS=200, and log all manifests (alias_catalog, endpoint_catalog, hierarchical, routing, fetch, joint selection_log + ablation logs) with hashes for audit. AUDIT must use stable metric/control IDs; DIRECTOR integrates only surviving evidence per research/EXPERIMENT_PACKET.md.

