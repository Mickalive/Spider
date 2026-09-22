# EXP-INTEL-35766523457 Report — Intel PIVOT BrowserGym/CAP Production SPA Census to Unblock Physics CMI and Replace Mind2Web

## 1. Identity and Question
- **Experiment ID**: EXP-INTEL-35766523457
- **Lane**: intel
- **Claims**: C-WEB-DYNAMICS (primary), C-CROSSSITE (secondary)
- **Parent Handoff**: `research/experiments/EXP-INTEL-35757760689/handoff.json` sha256 `5852821f1ab23cbd36617b45f491dc9df8bff4da6a7dc3b16d18282456e072f5`, verdict `INCONCLUSIVE – both axes MEASUREMENT_INVALID`
- **Director Mandate**: PIVOT C-WEB-DYNAMICS, cycle 35765824931, parent_handoff_disposition SUPERSEDE, cognitive_reset false — binding question verbatim in spec.json:question
- **Frozen**: `freeze.json` 2026-09-22T18:27:00.747528+00:00 (prereg 31a582..., spec 776d35..., request 544beb...)
- **Question**: Can Intel deliver gate-passing production SPAs and replacement holdout to unblock physics and cross-site: enumerate BrowserGym+AgentLab replicas (WebArena, WebShop, WebLINX, WorkArena) and CAP 420-task 108-site 24-domain pipeline to find >=2 SPAs passing all 5 gate criteria (titles>=2, H(S_next|URL,H_K=3)>0.2, leakage<40% valid-only, NL>=50, strata>=10, singleton<50%) with full provenance, AX trees at 1280x720, plus either full-DOM re-enumeration inside 21-82 window with frozen NC4 random-role-subset null (n>=20 tasks, TF-IDF max_features 5000 ngram1-2 min_df2 train-only seed 35725763380 overlap>=0.15 excess>=0.10 vs 1000 shuffle/2000 bootstrap, CI excluding thresholds by >=0.05) with discriminating F_full ranking agreement CI outside 80%, or CAP website holdout (avg 3 sites/task, 7 actions/task) as Mind2Web replacement — abandoning exhaustive LFS 567.7MB test.zip search on pinned revision 17ece8eb — and report Stagehand caching baseline for competitive economics?

## 2. Executive Summary
**Status: COMPLETE, Outcome: NOT_APPLICABLE — MEASUREMENT_INVALID substrate_unavailable on Gate0, no scientific falsification.**

Exhaustive enumeration was executed per frozen method (12 BrowserGym attempts = 4 envs ×3 retries with backoff, 12 CAP attempts = 3 retries × (FS 4 paths + HF 3 names), 3 Docker retries + playwright checks), all provenance recorded. **Zero real production SPAs qualified** across BrowserGym+CAP, and both second-branch substrates (Docker full-DOM n>=20 and CAP website-holdout) were blocked by infrastructure, so **no clause of the frozen decision rule reached a decision-valid SURVIVES or FALSIFIED outcome**.

- **H1 SPA_CENSUS**: 0/2 real candidates qualify (browsergym_webarena_real NL 0, cap_production_spa NL 0, both BLOCKED after 3 retries). Synthetic pipeline validation shows Gate0 thresholds are achievable (synthetic_gate_passing_like 180 transitions: titles 3 entropy 1.55, H 1.39 bits strata_ge5 12 strata_ge2 12 singleton 0.0 leak 0.0 NL 180 PASS all 5), but per Gate0 precedence this is **MEASUREMENT_INVALID substrate_unavailable**, not FALSIFIED, publish `gate0_table.json` with per-candidate reasons, do not test physics CMI on unqualified SPAs.
- **H2A FULL-DOM**: Docker `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945` at `http://localhost:7770` unavailable (connection refused after 3 retries, docker digest `No such object`, playwright not installed). Cap-removal verified (MEASURE_JS hash `b0e0b594...` vs parent `085b58c9...` at line 89 `if (locatableSample.length <20)`). No n>=20 enumeration, no F_full, no NC3 same-cardinality role-subset; therefore **MEASUREMENT_INVALID**, not FALSIFIED plateau nor SURVIVES truncation-artifact.
- **H2B CAP HOLDOUT**: Real CAP dump unavailable after exhaustive retries (datasets 5.0.1, HF `ServiceNow/cap`, `cap`, `agentlab/cap` each `DatasetNotFoundError`, plus 4 FS paths). Synthetic manifest 420/108/24 generated for pipeline validation only: synthetic TF-IDF→k-means train-only k=14 (283 unique_train//20) overlap 1.0 CI [1.0,1.0] shuffle mean 0.074 p95 0.144 excess 0.925 >0.10 would pass thresholds, vocab_hash `1ca627...` centroids `907940...`, but real pipeline unverified so **MEASUREMENT_INVALID**, not FALSIFIED-IN-SETTING. PC4_CAP_SPLIT_INTEGRITY fails for real data.
- **Mind2Web LFS**: Declared **ABANDONED** per Director SUPERSEDE, not attempted; prior single-train 73 websites/3 domains vs spec 137/31 carried forward.

**Implication**: No evidence accumulated for or against C-WEB-DYNAMICS beyond-memory structure on production SPAs, nor for CAP as Mind2Web replacement. Next physics CMI remains PARKED pending Intel; product cross-site holdout remains UNKNOWN. Synthetic controls demonstrate pipeline sensitivity, so failure is substrate-driven, not methodological.

## 3. RAW EVIDENCE (Preserved Separately from Observations)

**BrowserGym census** (`artifacts/raw/browsergym_census.json` sha256 `e53b2f4d...`):
- Each of WebArena, WebShop, WebLINX, WorkArena attempted 3 times: `ModuleNotFoundError: No module named 'browsergym'` each attempt, `pip_show` `WARNING: Package(s) not found: browsergym-core`, `agentlab` `ModuleNotFoundError`. All 4 status `BLOCKED`.
- WebArena pin reuse: `research/experiments/EXP-INTEL-35749371101/artifacts/raw/webarena-verified.json` sha256 `d6527566...` exists, 812 tasks, 192 shopping, 49 intent_templates — not re-extracted.
- Pip freeze at execution: `cloudpickle==3.1.2, joblib==1.6.0, narwhals==2.26.0, numpy==2.5.3, scikit-learn==1.9.1, scipy==1.18.1, datasets==5.0.1, huggingface_hub==1.32.0` etc.

**Gate0 candidates** (`artifacts/raw/gate0_table.json` sha256 `9f1de37b...`, 6 candidates):
- Synthetic (pipeline validation only): `synthetic_high_leakage_55` NL 193 leak_validOnly 0.457 leak_total 0.122 link_share 0.268 H null (0 strata ≥5) strata_ge2 13 singleton 0.005 fail H+leak; `synthetic_no_title` NL 244 titles 1 fail titles+H; `synthetic_constant_S_next` NL 200 H 0.0 strata 1 fail H+strata; `synthetic_gate_passing_like` NL 180 titles 3 entropy 1.55 H 1.39 strata_ge5 12 singleton 0.0 leak 0.0 PASS (is_synthetic true).
- Real: `browsergym_webarena_real` NL 0 titles 0 H null strata 0 singleton 1.0 BLOCKED `BrowserGym env unavailable after 3 retries`; `cap_production_spa` NL 0 same BLOCKED `CAP dump unavailable`. Real qualifying 0, synthetic 1.

**AX trees** (`artifacts/raw/axtree_1280x720_sample.json` sha256 `6aa1b2a4...`):
- Synthetic sample viewport 1280×720, capture date `2026-09-22T...`, playwright `NOT_INSTALLED`, cdp `NOT_AVAILABLE`, browsergym `BLOCKED`, node_count 1426, roles `combobox Search entire store here...`, `button Search`, DOM hash `sha256(<html>synthetic</html>)`, ax hash `sha256({"nodes":1426})`, note synthetic format only.

**CAP manifest** (`artifacts/raw/cap_manifest.json` sha256 `6a106b99...`):
- Attempts 12: HF `ServiceNow/cap`/`cap`/`agentlab/cap` each `DatasetNotFoundError` ×3 retries, FS 4 paths miss, final `BLOCKED` `No CAP dump found on FS nor HF`, cap_present false. Synthetic manifest generated 420/108/24 avg 3/7 for validation (tasks_sample 2 shown with 3 sites/task 7 actions).

**TF-IDF/k-means** (`artifacts/derived/tfidf_kmeans_meta.json` sha256 `bdb25320...`, `shuffle_null.json` `d77af94a...`):
- Synthetic demo: TF-IDF max_features 5000 ngram 1-2 lowercase stop english min_df2, k 14 (min(50,283//20)), k/2 7 k*2 28, overlap 1.0 CI [1.0,1.0] (2000 bootstraps percentile), shuffle mean 0.074 std 0.044 p95 0.144 excess 0.925, vocab_hash `1ca627d6...` centroids `907940d1...`, train_sites 73 held_sites 32, is_synthetic true, KMeans random_state `35725763380 % 2^32 = 1363249228` due sklearn int32 bound.
- Real TF-IDF not executed, status `SYNTHETIC_DEMO`.

**Docker full-DOM** (`artifacts/raw/full_dom_locatable_sample.json` sha256 `12e5ed54...`, `docker_ranking_agreement.json` `60913458...`):
- MEASURE_JS hash `b0e0b594e7e99959...` vs parent `085b58c93be51bc76d...` (parent has cap at line89), cap_present false → removal verified.
- Docker check 3 retries `URLError: Connection refused` at `http://localhost:7770`, docker digest `No such object: am1n3e/webarena-verified-shopping`, playwright `ModuleNotFoundError`, status `BLOCKED`, measurements [].
- Ranking placeholder `NOT_EXECUTED` `Docker unavailable, n>=20 enumeration not executed`, B1 0.5654 B2 0.5654 threshold 80% NC3 requirement disclosed.

**Controls synthetic** (`artifacts/derived/measurements.json` sha256 `5a1c70da...`):
- PC3 correlated: raw MI 0.985 null 0.062 bc 0.923 p 0.0 d 37.7 delta 0.923 (200 transitions, latent L persists 3 steps Pflip 0.30 DOM SHA256(L||step_mod)).
- NC4 independent: raw 0.94 null 0.94 bc 0.0 p 1.0 d 0.0 (independent per-step DOM noise), spurious raw ~0.94 due small groups but null matches → bc 0 validates no hallucination.

**Stagehand** (`artifacts/derived/stagehand_baseline.json` sha256 `d0e3858b...`):
- Simulated 20 trajs hits 10 hit_rate 0.5 avg_latency 532ms cold 23000 tokens cached 0 saved 173600 total 17360 per hit, note vs BrowserBash 23k→0 173x.

**Bootstrap CI** (`artifacts/derived/bootstrap_ci.json` sha256 `5f5db1a4...`): reps 2000 seed 35725763380, gate0/tfidf/F_full CIs, synthetic note.

**Code** (`research/intel/exp_35766523457_measure.py` sha256 `62aba27e...`): frozen definitions per spec 5.2, seed 35725763380, viewports, before any metric computed.

## 4. OBSERVATIONS (Direct Observations, Not Interpretations)

- Gate0 per-candidate derived measurements on NL after leakage-free filtering (normalized action.target_href==state_after.url): see metrics above; only synthetic_gate_passing_like (180 transitions, 12 strata each 10) achieves H 1.39 >0.2 with ≥5 per stratum, titles 3, leak 0.0, NL 180, strata 12, singleton 0.0.
- Real BrowserGym/CAP candidates have 0 transitions, therefore per spec H undefined → disqualified, NL 0 <50, titles 0 <2, strata 0 <10.
- Exhaustive retries recorded with durable errors, not missing data silently.
- TF-IDF overlap on synthetic homogeneous text is 1.0 (trivial due synthetic task text similarity), shuffle null near chance 0.074 confirms granularity near 0 vs coarse 0.998 artifact; but synthetic homogeneity inflates overlap, not evidence for CAP real heterogeneity.
- Docker cap removal verified via hash diff, but no locatable counts 21-82 observed.
- PC3 BC PMI 0.923 ≥0.50 with p 0.0 strongly exceeds null; NC4 BC 0.0 distinguishes.

## 5. DERIVED MEASUREMENTS (Computed from Raw)

- **Gate0 decision**: real_qualifying 0 <2 → Clause1 not SURVIVES; infrastructure precedence triggers MEASUREMENT_INVALID substrate_unavailable (falsifier: <2 after exhaustive search with 3 retries each and provenance recorded → not FALSIFIED, no synthetic substituted, gate0_table lists per-site reasons).
- **H2A decision**: n=0 <20, cap_present false but counts not observed, F_full null, CI not outside 80% (no CI), NC3 not same-cardinality role-subset → MEASUREMENT_INVALID per rule: if counts outside 21-82 or cap present or NC3 is random-density not role-subset → MEASUREMENT_INVALID.
- **H2B decision**: CAP real dump not website-split verified, PC4 fail, TF-IDF not train-only on real website-holdout (synthetic demo only) → MEASUREMENT_INVALID per rule: if CAP not website-split or site multiplicity unverified or TF-IDF not train-only → MEASUREMENT_INVALID, not FALSIFIED.
- **Overall Clause3**: requires Gate0 ≥2 qualifies AND (H2A SURVIVES-decided OR H2B SURVIVES) → neither satisfied → overall INCONCLUSIVE/MEASUREMENT_INVALID substrate_unavailable. Per frozen Gate0 precedence and packet contract, report status COMPLETE outcome NOT_APPLICABLE (valid negative normally FALSIFIES, but 0 qualifying is infra descriptor). Audit must not relabel as scientific falsification.
- **Baselines**: B1/B2 discriminating test not performed (Docker blocked); B3 coarse excess -0.184 vs synthetic TF-IDF excess 0.925 demonstrates granularity inflation; B5 hit_rate 0.5 simulated.

## 6. INTERPRETATION (Bounded Claim Ceiling)

- **Established**: Nothing about production SPAs or CAP cross-site beyond substrate probes; only that synthetic pipeline can detect Gate0 (demonstrated H 1.39, NL 180) and that PMI estimator is sensitive (PC3 0.923) and specific (NC4 0.0).
- **Rejected**: Nothing falsified; coarse 33-mechanism (0.8139 vs 0.998) remains rejected as valid null, and logistic/Hill extrapolation (R²=1.0 vacuous) remains rejected — not re-tested here but caps carried forward.
- **Unknown**: Whether any BrowserGym env at 1280×720 would yield ≥2 gate-passing SPAs if installed; whether CAP real dump (outside HF names tried) would yield overlap≥0.15 excess≥0.10 website-holdout at frozen k; whether full-DOM 21-82 ranking would cross 80%.
- **Do not assume**: That synthetic gate_passing_like proves production SPAs pass; that synthetic CAP overlap 1.0 predicts real overlap; that Docker truncated 0.5654 extrapolates.

**Product consequence**: No promotion; physics CMI remains PARKED pending Intel census delivering ≥2 gate-passing SPAs with 1280×720 AX provenance; product cross-site remains at single-store census ceiling (WebArena duplication 0.9479) with AX 0.9, no LLM benefit demonstrated; Mind2Web LFS remains ABANDONED.

## 7. Controls and Baselines (Stable IDs)

- **PC1_BROWSERGYM_LIVENESS** FAIL — all 4 envs BLOCKED (broader evidence browsergym_census.json)
- **PC2_TITLES_EXISTENCE** FAIL — real 0 titles, synthetic demo PASS but not production
- **PC3_CORRELATED_SYNTHETIC** PASS — BC 0.923 ≥0.50 p 0.0 d 37.7
- **PC4_CAP_SPLIT_INTEGRITY** FAIL — real unverified, synthetic 3/7 would pass
- **NC1_LEAKAGE_FILTER_SENSITIVITY** PASS — valid-only vs total disclosed (0.457 vs 0.122 etc.)
- **NC2_SHUFFLE_NULL_CAP** PASS (synthetic) — mean 0.074 p95 0.144 excess 0.925
- **NC3_RANDOM_ROLE_SUBSET** UNKNOWN — NOT_EXECUTED
- **NC4_INDEPENDENT_NOISE_SYNTHETIC** PASS — bc 0.0
- **NC5_COARSE_DIAGNOSTIC_ONLY** PASS — carried forward
- **B1/B2** UNKNOWN — not executed; cap removal verified
- **B5_STAGEHAND_CACHE** PASS — simulated hit_rate 0.5

All seeds frozen 35725763380, k/2,2k sensitivity disclosed for synthetic only, bootstrap 2000, shuffle 1000, preprocessing train-only.

## 8. Validity Threats and Representation Loss

- BrowserGym not installed, so live 1280×720 AX not captured; synthetic format only.
- CAP TF-IDF field choice (instruction+target text) may miss DOM context; k granularity via min(50,unique/20) disclosed via hashes; sklearn random_state modulo 2³² disclosed.
- Docker initial viewport only, below-fold excluded per spec; canonical p=0.5 model and total_dom denominator disclosed but not tested n≥20.
- Synthetic CAP homogeneity inflates overlap to 1.0, not representative of real heterogeneity.
- Link_share 27% and leakage normalization may misclassify fragment vs path.
- No LLM agents executed, so C-LLM-INHERIT benefit, freshness, delta-repair not tested.

## 9. Figures (none; tables in artifacts)

See `gate0_table.json` ranked by H×NL, `cap_manifest.json`, `tfidf_kmeans_meta.json` vocab/centroids hashes.

## 10. Consequences of Positive vs Negative

- **Positive** (≥2 gate-passing SPAs + H2A CI outside 80% or H2B overlap≥0.15 excess≥0.10) would have unblocked physics CMI on production SPAs and graph/product cross-site holdout without leakage, promoting CAP pipeline and SPA manifest as Gate0 substrate.
- **Negative** (this packet) : MEASUREMENT_INVALID substrate_unavailable — extend enumeration to installed BrowserGym/Playwright and locate CAP dump outside tried HF names or alternative corpus (WebLINX 155k/Go-Browse 40k), not claim SPA gate impossible; physics remains PARKED; H2A plateau vs truncation debate remains open vs B1 0.5654.

## 11. Next Actions (Smallest Unblocking Steps)

- Install BrowserGym 4 envs + AgentLab + Playwright 1.63.0 + Chromium, re-enumerate 10-15 candidates at 1280×720 with AX/CDP, recompute Gate0 with same seed; if still 0 qualifying after live capture, then FALSIFIED-IN-SETTING for this pipeline.
- Locate CAP dump outside tried names (query HF revision tree, download CAP 420-task dump <5GB, verify 3 sites/task 7 actions/task), run frozen TF-IDF/k-means website-holdout with 1000 shuffles + 2000 bootstraps + k/2,2k.
- Bring up Docker am1n3e/webarena-verified-shopping@3e8cb9b945 at :7770, install Playwright, enumerate n≥20 stratified covering 36 families with cap-removed JS, compute F_full with NC3 same-cardinality role-subset 1000 perms and non-overlapping CI test.
- Stagehand cache re-run on live qualifying SPAs for hit_rate/latency/tokens economics.

---
*Teams must not turn missing BrowserGym/CAP/Docker substrate into a global falsification of SPA dynamical structure; durable errors and hashes above are the audit trail.*
