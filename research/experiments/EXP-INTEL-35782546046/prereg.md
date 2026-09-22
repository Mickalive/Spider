# EXP-INTEL-35782546046 preregistration — intel PIVOT (Director SUPERSEDE, cognitive_reset true)

**Lane:** intel  
**Experiment:** EXP-INTEL-35782546046  
**Director mandate:** PIVOT on C-LLM-INHERIT (comparative reasoning: exhaustive 1280x720 AX + CAP 420-task + WebArena full-DOM strict Gate0 0/3 MEASUREMENT_INVALID due to BrowserGym/AgentLab pin nonexistent; fresh view pivots to narrow feasible unblock with relaxed Gate0 pilot and Stagehand baseline)  
**Parent handoff:** research/experiments/EXP-INTEL-35773136560/handoff.json — SUPERSEDE, not CONTINUE. Established/rejected/unknown/do_not_assume below are continuity evidence only per AGENTS.md global direction discipline.  
**Frozen before outcome:** DESIGN ONLY — no outcome-bearing measurements inspected.  
**Seed:** 35725763380 (all sampling, shuffles, bootstraps; KMeans int32 seed 1363249228 = 35725763380 mod 2^32 if KMeans used descriptively).  
**Substrate:** WebArena-Verified v2 shopping Docker am1n3e/webarena-verified-shopping@sha256:3e8cb9b945 at http://localhost:7770, BrowserGym-core 0.14.3 + AgentLab 0.4.2 primary (0.3.0 fallback, NOT 0.14.3) + Playwright 1.63.0 Chromium, 1280x720 initial viewport no scroll, CDP Accessibility.getFullAXTree.

---

## 1. Question and inherited state

**Director question (frozen):** After pinning BrowserGym-core 0.14.3 with correct AgentLab release (0.3.0/0.4.2, not nonexistent 0.14.3) and Playwright 1.63.0 at 1280x720, can 20 live CDP Accessibility.getFullAXTree captures (10 families x2, longest-prefix element-pattern without fallback, task-specific start_url category/product/cart, seed 35725763380) on WebArena-Verified v2 shopping Docker achieve AX_consistency >=0.6 (vs prior 0.2857 invalid and 0.9 single-family pass) to demonstrate identifiable same-mechanism parameterized transfer, and can Stagehand server-side caching (selector+DOM-hash, HIT/MISS after N identical results, per-project scope) be replicated on the same 36 families to report cache hit rate, 2x speedup and ~30% cost vs flat RAG-EMBED vs SPIDER reconstruction false_accept, thereby delivering the strong baseline and the relaxed Gate0 census that unblocks physics (H>0.1, NL>=20, titles>=1) and product C-LLM-INHERIT/C-RESIDUAL-NOVELTY without exhaustive 567.7MB LFS test.zip / CAP 420-task exhaustive search?

**Priority claims:** C-LLM-INHERIT (target), plus C-CROSSSITE and C-PRODUCT-ECON as affected downstream.  
**Registry status:** C-LLM-INHERIT HYPOTHESIS, C-CROSSSITE HYPOTHESIS, C-PRODUCT-ECON HYPOTHESIS (no claim has reached VALIDATED on live substrate; prior synthetic-only C-SEMANTIC-RESOLVE and Bayesian K12 are not live evidence).

**Inherited established (carry forward, not re-measured as SURVIVES this cycle):**
- WebArena-Verified v2 pin d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30 (812 total, 192 shopping, 36 families >=3) duplication 0.9479, parameterized 0.8958 — reused for family sampling only.
- Within-store element-pattern AX_consistency=0.9 CI[0.7,1.0] longest-prefix without fallback (single family, audit PASS) — prior positive control, to be re-tested on 10 families.
- Synthetic gate_passing_like NL180 H1.39 and PC3 correlated SPA PMI 0.923 and NC4 independent noise 0.0 — pipeline validation only (is_synthetic true), not production evidence.
- Cap-removal MEASURE_JS hash b0e0b594 verified (no locatableSample.length<20 cap) — not needed this cycle but recorded.
- Exhaustive probe errors (12 BrowserGym ModuleNotFoundError, 15 CAP DatasetNotFoundError, Docker connection refused, playwright missing) map to MEASUREMENT_INVALID per Gate0 precedence — retained as rationale for SUPERSEDE.
- AgentLab==0.14.3 is nonexistent (pip proves 0.3.0/0.4.2) — corrected here.

**Inherited rejected (must not assume):**
- 12-store cross-site M1=1.0 on v2 single Magento store; model-extrapolation L=0.5654/R2=1.0 vacuous; coarse 33-mechanism overlap 0.8139 vs null 0.998 as TF-IDF proxy; 0 qualifying strict Gate0 as global falsification; Mind2Web LFS as required path.

**Unknowns this experiment narrows (from handoff unknown 1,4,6,7,8,9):**
- Whether 10 families x2 at corrected pins at 1280x720 yields AX_consistency >=0.6 vs shuffle null (this H1 directly tests).
- Whether Stagehand selector+hash caching yields HIT/MISS discrimination and 2x/~30% on 36 families vs RAG-EMBED/SPIDER false_accept (this H2 directly tests).
- Whether relaxed Gate0 (H>0.1 NL>=20 titles>=1) is achievable even though strict Gate0 0/3 prior fails (this H3 census reports).
- Which AgentLab version actually provides 0.14.3 compatibility (record 0.4.2 vs 0.3.0).

**Do-not-assume guards:** Synthetic 1.0 overlap or 0.923 PMI does not imply production AX_consistency; 0/3 strict Gate0 does not imply relaxed 0/10; truncated 0.5654 does not predict full-DOM; simulated Stagehand 0.5 does not imply measured hit_rate; AX 0.9 single-family does not imply 10-family mean.

---

## 2. Hypotheses

**H1_AX_CONSISTENCY (confirmatory):** Mean AX_consistency across 10 families (2 tasks each, longest-prefix without fallback at 1280x720) >=0.6 with bootstrap 95% CI lower >0.5 and permutation p<0.05 vs family-label shuffle null and delta >=0.20 above prior invalid 0.2857, demonstrating identifiable same-mechanism parameterized transfer within WebArena-Verified v2 shopping.

**H2_STAGEHAND_BASELINE (confirmatory):** Stagehand server-side selector+DOM-hash verb cache (exact selector + DOM-hash SHA256, HIT after N=2 identical results, per-project scope) replicated on >=30/36 families reports hit_rate, speedup (cold/cached latency) and tokens_saved with HIT on identical DOM >=0.8, MISS on drifted DOM >=0.8, false_accept <0.05 and beats random cache null p<0.05, delivering shipped baseline comparison vs flat RAG-EMBED and SPIDER 0-token reconstruction.

**H3_RELAXED_GATE0_CENSUS (descriptive):** On same 20 captures, relaxed Gate0 pass count (titles>=1, H>0.1 with >=5 per stratum, NL>=20, singleton<50%) and strict Gate0 pass count (titles>=2, H>0.2, NL>=50, strata>=10, leakage_validOnly<40%) reported with bootstrap CIs; >=1 relaxed pass suggests next physics can run correlated-state pilot H>0.1 pilot without exhaustive search.

---

## 3. State, action, target, observable

**State representation:** Raw CDP Accessibility.getFullAXTree nodes (role, name, value, properties) plus DOM outerHTML subtree hash for Stagehand key. No PCA/TF-IDF embedding for AX_consistency; longest-prefix pattern operates on normalized selector patterns (tokenized selector path). Title = document.title string; URL = normalized page URL (lowercase, strip query/fragment for leakage). H computed on state defined as (URL, H_K=3 history) if H needed for census (same as prior physics).

**Action representation:** Element-pattern: normalized selector pattern derived from AX node + DOM attributes for target element (e.g., role+name+CSS path). Longest-prefix: longest common prefix of tokenized pattern (>0 tokens) across family tasks, no fallback to nearest-neighbour semantic or TF-IDF.

**Target/observable:** Primary metric M-AX-CONSISTENCY = mean per-family indicator (1 if both tasks in family map to same longest-prefix pattern, else 0) across 10 families. Range [0,1]. Secondary: M-STAGEHAND-HITRATE, M-STAGEHAND-SPEEDUP, M-STAGEHAND-TOKENS-SAVED, M-STAGEHAND-FALSE-ACCEPT. Census: M-GATE0-RELAXED-PASS count and M-GATE0-STRICT-PASS count.

**Unit of analysis:** Family for H1 (n=10 families, 20 tasks), per-family task for Stagehand (n=36 families, up to 72 tasks if 2 per family).

---

## 4. Sampling policy

- **Family sampling:** From 36 WebArena-Verified v2 shopping families with >=3 tasks (census 36 ge3), sample 10 families without replacement using seed 35725763380 (Python random, deterministic). Stratify not required; record which 10 chosen with artifact hash.
- **Task sampling:** Within each of the 10 families, sample 2 distinct tasks without replacement (seed 35725763380) prioritizing distinct start_url categories (category, product, cart) if family has those; task IDs pinned in artifact.
- **Stagehand replication:** Attempt all 36 families (>=30 required for H2 validity), sampling 2 tasks per family where possible (same families as H1 plus remaining 26); seed 35725763380 reused.
- **No CAP/Online-Mind2Web/Mind2Web LFS sampling this cycle** — explicitly ABANDONED per Director SUPERSEDE; not measured.
- **Start_url:** Task-specific start_url per WebArena-Verified task definition (category listing, product detail, cart). No cross-family leakage.

---

## 5. Holdout and contamination controls

- AX_consistency has no train/test split — it is within-family consistency of longest-prefix, no fitting on held-out families. No TF-IDF/k-means training to leak.
- Stagehand cache: keys fitted on first occurrence per (project, selector, hash) and tested on second occurrence within same family (intra-family HIT test) and cross-project isolation test; no cross-family key reuse that would inflate hit_rate.
- All 20 AX captures captured at 1280x720 initial viewport no scroll; below-fold or post-interaction AX after scroll/add-to-cart not included (would be representation shift per handoff do_not_assume).
- BrowserGym/AgentLab/Playwright versions pinned and recorded; no post-hoc pin change after seeing AX scores.

---

## 6. Nulls, baselines, and controls (stable IDs)

**Baselines:**
- B-STAGEHAND-VERB (shipped Feb 2026 exact selector+hash 2x/~30%, per-project) — H2 must match definition.
- B-RAG-EMBED-FLAT (flat retrieval without DOM-hash guard) — hit vs false_accept comparison.
- B-SPIDER-0TOKEN (verbatim replay 0 tokens on HIT, 0% on novel) — token economics floor.
- B-RANDOM-AX-SHUFFLE (1000 perms family-label shuffle for AX) — null for H1 discrimination.
- B-CONSTANT-NULL-05654 (REJECTED vacuous 0.5654) — disclosed only to prevent extrapolation reuse.
- B-COLD-LLM (cold agent from scratch, same model/tools/budget) — descriptive upper bound, not executed.

**Positive controls:**
- PC1_AX_LIVENESS_1280: >=15/20 AX trees 600-2000 nodes, DOM bytes >=2000, Docker reachable after 3 retries.
- PC2_AX_PRIOR_REPLICATION: >=1 family replicates prior 0.9 CI[0.7,1.0] within-family.
- PC3_STAGEHAND_HIT_IDENTICAL: On stable family with 3 identical DOM-hash+selector, HIT on 2nd/3rd call with per-project isolation.
- PC4_SYNTHETIC_PIPELINE: Synthetic validation retained but is_synthetic true, not decision.

**Null controls:**
- NC1_AX_SHUFFLE_NULL: 1000 family-label perms seed35725763380, true must exceed p95 and mean+0.30, p<0.05.
- NC2_AX_RANDOM_PATTERN: Random pattern from different family <0.2 expected.
- NC3_STAGEHAND_DOM_DRIFT: Single-attribute DOM mutation expecting MISS; false_accept <0.05.
- NC4_STAGEHAND_RANDOM_CACHE: Random HIT/MISS shuffling ~0.5 hit_rate, ~1.0 speedup; true must beat.
- NC5_CROSS_PROJECT_LEAKAGE: Same key different project must MISS, cross-project HIT 0%.

---

## 7. Primary metric and expected direction

**Primary confirmatory metric:** M-AX-CONSISTENCY (mean [0,1]) with bootstrap 95% CI and NC1 shuffle null.
**Expected direction under H1:** True >=0.6 and CI lower >0.5 and permutation p<0.05 and delta vs 0.2857 >=0.20.
**H2 primary:** M-STAGEHAND-HITRATE and M-STAGEHAND-FALSE-ACCEPT with speedup; expected HIT >=0.8, false_accept <0.05.

No threshold changed after seeing outcomes. Ordinal handling frozen as longest-prefix without fallback only.

---

## 8. Uncertainty method and resampling unit

- Bootstrap 2000 percentile 95% CIs for M-AX-CONSISTENCY (resampling families, not tasks, to respect family-grouped dependency) and for Stagehand hit_rate (resampling families).
- Permutation 1000 for NC1 shuffle null (permute family labels across 10 families, preserve per-family 2 tasks), seed 35725763380; report mean/std/p95 and permutation p = (1 + count perm >= true)/(1+1000).
- All seeds deterministic; Python hash randomization not used (site pin via string compare). Resampling unit = family for AX, family/task for Stagehand hit_rate.

---

## 9. Adequacy and validity rules

**Adequate H1 run:** >=10 families (20 trees) with node counts 600-2000, viewport 1280x720, CDP hash recorded, longest-prefix without fallback verified by code hash; else MECHANISM_INVALID insufficient data.  
**Adequate H2 run:** >=30/36 families attempted with selector+hash cache logic (N=2, SHA256, per-project); else MEASUREMENT_INVALID.  
**Adequate census:** Raw transitions per capture recorded even if <50; H undefined if <5 per stratum flagged and excluded from H gate but still reported.  
**Representation loss disclosed:** Longest-prefix pattern only, initial viewport only, CDP AX vs full DOM, DOM-hash subtree outerHTML choice, N=2.

---

## 10. Falsification / survival / invalidity rules (frozen)

```
IF Docker/CDP yields <5 families (<10 trees) after 3 retries + Playwright verify:
  H1 = MEASUREMENT_INVALID substrate_unavailable (status COMPLETE outcome NOT_APPLICABLE)
  publish failure provenance, do not falsify
ELIF captured >=10 families:
  IF mean AX_consistency >=0.6 AND ci_lower >0.5 AND perm_p <0.05 AND delta_vs_0.2857 >=0.20 AND PC1 >=15/20:
    H1 = SURVIVES (parameterized transfer identifiable at longest-prefix)
  ELSE:
    H1 = FALSIFIED-IN-SETTING (bounded to WebArena v2 shopping longest-prefix method)

IF Stagehand attempted <30/36 families due to Docker unavailability:
  H2 = MEASUREMENT_INVALID
ELIF attempted >=30:
  IF hit_on_identical >=0.8 AND miss_on_drift >=0.8 AND false_accept <0.05 AND speedup/tokens reported AND beats NC4 p<0.05:
    H2 = SURVIVES (baseline replicable)
  ELSE:
    H2 = FALSIFIED-IN-SETTING (selector+hash not discriminating here)

H3 census descriptive:
  Report relaxed_pass = count families/titles>=1 & H>0.1 & NL>=20 & singleton<50
  and strict_pass = count with titles>=2 & H>0.2 & NL>=50 & strata>=10 & leakage<40%
  with bootstrap CIs; >=1 relaxed pass suggests next physics relaxed pilot feasible.

Overall SURVIVES if H1 SURVIVES and H2 at least reporting valid (preferred both SURVIVES);
H1 FALSIFIED alone is sufficient to reject this AX method for product within-store claim.
No CAP/LFS exhaustive search changes this verdict.
```

All control/baseline identifiers and metric IDs are frozen for EXECUTE/AUDIT recomputation: B-STAGEHAND-VERB, B-RAG-EMBED-FLAT, B-SPIDER-0TOKEN, B-RANDOM-AX-SHUFFLE, B-CONSTANT-NULL-05654, B-COLD-LLM, PC1_AX_LIVENESS_1280, PC2_AX_PRIOR_REPLICATION, PC3_STAGEHAND_HIT_IDENTICAL, NC1_AX_SHUFFLE_NULL, NC2_AX_RANDOM_PATTERN, NC3_STAGEHAND_DOM_DRIFT, NC4_STAGEHAND_RANDOM_CACHE, NC5_CROSS_PROJECT_LEAKAGE, M-AX-CONSISTENCY, M-AX-CI-LOWER, M-AX-SHUFFLE-P, M-STAGEHAND-HITRATE, M-STAGEHAND-SPEEDUP, M-STAGEHAND-TOKENS-SAVED, M-STAGEHAND-FALSE-ACCEPT, M-GATE0-RELAXED-PASS, M-GATE0-STRICT-PASS.

---

## 11. Product consequence

**Positive (H1 SURVIVES + H2 reporting):** Delivers measurement-valid within-store parameterized transfer (10 families, correct pins, longest-prefix >=0.6) and shipped Stagehand baseline (hit_rate/speedup/~30% vs RAG-EMBED vs SPIDER false_accept) — product can decide Stagehand vs SPIDER investment and physics can run relaxed H>0.1 NL>=20 pilot on same families without inventing 4-point extrapolation or 567.7MB LFS. Artifacts become substrate for next physics/product holdout.

**Negative (H1 FALSIFIED or H2 FALSIFIED or MEASUREMENT_INVALID):** If FALSIFIED, this longest-prefix method does not achieve identifiable transfer or Stagehand not discriminating on shopping families — product must try alternative pattern grammar or use RAG-EMBED baseline; if MEASUREMENT_INVALID (0 families after 3 retries), no falsification, repair Docker/pins and re-run orthogonal BrowserGym loopback/hierarchical retrieval, not exhaustive LFS/CAP.

---

## 12. Cost and information

**Cost:** LOW-MEDIUM, no LLM calls, Docker (~1-2GB) + BrowserGym-core 0.14.3 + AgentLab 0.4.2/0.3.0 + Playwright 1.63.0 Chromium (~300MB), 20 AX captures + 36-family Stagehand sweep ~2-2.5h, <10GB /tmp.  
**Information:** MAXIMUM per Director comparative reasoning — directly tests last-mile blocker (0.2857 invalid method fix) with correct pins and delivers competitive baseline that determines SPIDER vs Stagehand product decision and unblocks physics relaxed pilot, beating another synthetic bandwidth or vacuous F=0.5654 tuning (diminishing after 44 frontier tunnel).

---

## 13. Execution plan (frozen, no outcome inspection)

1. Pin and verify: pip install browsergym-core==0.14.3 agentlab==0.4.2 (fallback 0.3.0) playwright==1.63.0, playwright install --with-deps, record pip freeze hashes, verify CDP.
2. Bring up Docker am1n3e/webarena-verified-shopping@sha256:3e8cb9b945 at http://localhost:7770, record digest, sample 10 families from 36 (>=3) seed35725763380, 2 tasks per family with task-specific start_url.
3. Capture 20 AX trees via CDP at 1280x720 initial no scroll (600-2000 nodes), compute AX_consistency longest-prefix without fallback, bootstrap 2000, shuffle 1000.
4. Replicate Stagehand selector+hash (N=2, SHA256, per-project) on 36 families, inject DOM drift, test cross-project isolation, report hit_rate/speedup/tokens/false_accept vs RAG-EMBED flat and SPIDER 0-token.
5. Compute relaxed vs strict Gate0 census on same 20 captures (titles, H with >=5/stratum, NL, strata, leakage_validOnly, singleton).
6. Preserve raw artifacts with sha256 and provenance; disclose representation loss; no CAP/LFS exhaustive search.

