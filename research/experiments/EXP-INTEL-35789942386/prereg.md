# EXP-INTEL-35789942386 preregistration — intel REOPEN (Director REOPEN C-CROSSSITE, cognitive_reset true)

**Lane:** intel  
**Experiment:** EXP-INTEL-35789942386  
**Director mandate:** REOPEN C-CROSSSITE — fix __SHOPPING__/path placeholder to deliver measurement-valid AX_consistency on product pages, spec-compliant Stagehand selector+subtree with drift, and relaxed Gate0 via multi-step BrowserGym rollouts (no exhaustive LFS/CAP)  
**Parent handoff:** research/experiments/EXP-INTEL-35782546046/handoff.json — USE (continuity evidence, not agenda). Established/rejected/unknown/do_not_assume distinctions preserved below per AGENTS.md.  
**Frozen before outcome:** DESIGN ONLY — no outcome-bearing measurements inspected; spec/prereg freeze before execution.  
**Seed:** 35725763380 (all sampling, shuffles, bootstraps; deterministic)  
**Substrate:** WebArena-Verified v2 shopping Docker am1n3e/webarena-verified-shopping@sha256:3e8cb9b945 at http://localhost:7770, BrowserGym-core 0.14.3 + AgentLab 0.4.2 primary (0.3.0 fallback if incompatible) + Playwright 1.63.0 primary (1.44.0 fallback if 1.63.0 incompatible with browsergym-core) at 1280x720, CDP Accessibility.getFullAXTree. No CAP/Online-Mind2Web LFS exhaustive search.

---

## 1. Question and inherited state

**Director question (frozen, binding per request.json director_mandate):** After pinning BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.63.0 at 1280x720 and fixing __SHOPPING__/path placeholder expansion to task-specific product/category/cart pages (not ?task= homepage), does N=20 live CDP Accessibility.getFullAXTree captures (10 families x2, longest-prefix without fallback, seed 35725763380) achieve AX_consistency >=0.6 (2000 bootstrap CI lower>0.5, 1000 shuffle null p<0.05, delta>=0.2 vs prior 0.2857 invalid and discrimination vs 0.9 single-family inflated), and can Stagehand selector+DOM-hash caching replication report HIT/MISS >=0.8 false_accept<0.05 (NC4 random null p<0.05, cold vs cached latency/tokens) plus relaxed Gate0 census (H>0.1 NL>=20 titles>=1) delivering multi-step BrowserGym rollouts to unblock physics/product without exhaustive 567MB LFS / CAP 420-task search?

**Design refinement (smallest high-information falsifiable conversion):** Same question converted to executable gates: (a) fix get_task_start_url to expand `__SHOPPING__/path` -> `http://localhost:7770/path` (not only exact `__SHOPPING__`), re-capture 20 AX trees on task-specific product/category/cart pages (not homepage), compute longest-prefix without fallback mean 95% CI and shuffle null with variance>0 check; (b) re-derive Stagehand key from AX node+DOM normalized selector and relevant-subtree SHA256 (not synthetic fam_task + full-page hash), execute drift MISS and random null with real-path latency/tokens; (c) collect multi-step BrowserGym trajectories (>=50 transitions) for relaxed Gate0 (H>0.1 NL>=20) vs strict, on same families. No exhaustive 420-task/567MB LFS or CAP outside ServiceNow/cap attempted (ABANDONED per Director SUPERSEDE).

**Priority claims:** C-CROSSSITE (target per mandate, primary), C-LLM-INHERIT and C-PRODUCT-ECON as downstream affected (single-store within-store transfer and shipped baseline economics). Registry status: all HYPOTHESIS on live substrate (C-CROSSSITE HYPOTHESIS, C-LLM-INHERIT HYPOTHESIS, C-PRODUCT-ECON HYPOTHESIS); prior synthetic-only or single-family 0.9 not live cross-site evidence.

**Inherited established (carry forward, not re-measured as SURVIVES this cycle — verbatim from handoff carry_forward.established):**
- WebArena-Verified v2 shopping substrate replicated: 192 tasks, 49 intent_templates, 36 families >=3 (34 >=4, 33 >=5), duplication 0.9479 95%CI [0.9167,0.9792] exact-copy 0.0781 param_task 0.8958 [0.8540,0.9375] — artifacts/raw/webarena_census.json sha1923e6fa
- Substrate stack LIVE at 1280x720 initial viewport no scroll: Docker am1n3e/webarena-verified-shopping@sha256:3e8cb9b945 reachable after 1 retry on 7770, BrowserGym-core 0.14.3 + AgentLab 0.4.2 + Playwright 1.44.0 + Chromium v1117 CDP Accessibility.getFullAXTree functional with 16/20 valid captures 1430 nodes 600-2000 window, DOM bytes>>2000 — artifacts/raw/ax_captures.jsonl sha0e022eb8
- Sampling integrity preserved: seed 35725763380 deterministic for family sampling [136,208,211,172,191,139,138,222,101,194], bootstrap 2000 percentile family-level and 1000 shuffle perms, Docker digest and provenance hashes recorded — provenance.json sha a2e327a2
- Within-store element-pattern prior single-family AX_consistency 0.9 CI[0.7,1.0] longest-prefix without fallback remains prior positive control (EXP-INTEL-35749371101) but not replicated on diverse pages here — report.md PC2 PARTIAL
- Gate0 precedence and exhaustive-search ABANDONED per Director SUPERSEDE: no CAP 420-task/108-site or Mind2Web LFS 567MB test.zip or WebJudge-7B required; CAP outside ServiceNow/cap exhaustive 12+15 attempts MEASUREMENT_INVALID retained as rationale — spec.json measurement_validity #6

**Inherited rejected (bounded, must not assume — from handoff carry_forward.rejected):**
- Bounded rejection A: AX_consistency mean 1.0 CI[1.0,1.0] p=1.0 on 8 homepage-identical families is NOT discriminating evidence for identifiable same-mechanism parameterized transfer via longest-prefix; reflects page identity not transfer — does NOT reject longest-prefix method on task-specific product/category/cart pages (unmeasured due to placeholder bug)
- Bounded rejection B: Stagehand replication with synthetic selector fam{id}_task{id} + full-page outerHTML hash, microsecond dict-lookup latency and hardcoded 1000 tokens, hit_rate 0.941 (64/68) without NC3 drift MISS or NC4 random null is NOT spec-compliant replication of shipped Stagehand Feb 2026 exact selector+DOM-hash HIT after N=2 per-project 2x/~30% baseline
- Bounded rejection C: Relaxed Gate0 0/16 and strict 0/16 on 16 single-page viewport-only captures (NL0 strata1 singleton1.0 H undefined) is descriptive viewport-only census, not evidence for/against relaxed Gate0 feasibility (H>0.1 NL>=20) on multi-step trajectories
- Prior closed path remains: 6-model density extrapolation to full-DOM n=50/82 as L=0.5654 logistic (4 points/3 params, k=10.75 saturates, Hill h=20 at bound) is informationally vacuous and definitively CLOSED — Docker direct full-DOM measurement is only remaining path (EXP-INTEL-35551517470 audit VF2-VF4)
- Prior coarse 33-mechanism overlap 0.8139 and model-extrapolation L=0.5654 as TF-IDF proxy for C-CROSSSITE is REJECTED as vacuous vs null 0.998; single-store v2 overlap vacuous by construction not cross-site evidence

**Unknowns this experiment narrows (from handoff unknown 1-6):**
- Whether fixing placeholder and capturing task-specific product pages for all 10 families x2 yields discriminating AX_consistency variance, CI lower>0.5, shuffle p<0.05 and delta>=0.2 vs prior 0.2857, discriminating vs 0.9 inflated single-family
- Whether Stagehand N=2 selector+relevant-subtree SHA256 on product pages achieves MISS>=0.8 false_accept<0.05 beats NC4 random null and measures ~2x/30% vs cold LLM / RAG-EMBED / SPIDER-0TOKEN
- Whether multi-step BrowserGym trajectories (>=50 transitions) yield >=1 relaxed Gate0 pass (titles>=1 H>0.1 NL>=20) to unblock physics correlated-state pilot, and whether strict ever passes on shopping
- Which Playwright version (1.63.0 spec vs 1.44.0 installed due to browsergym-core constraint) is correct pinned version, and AgentLab 0.3.0 vs 0.4.2 fidelity
- Whether alternative pattern grammars (semantic, subtree, multi-anchor) or shopping_admin 184 tasks 42 families would outperform
- Whether inclusion of 4 previously failed families (136,222) with product-page distribution changes mean directionally

**Do-not-assume guards (from handoff do_not_assume, binding):**
- Do not assume homepage 1.0 implies product-page transfer; zero variance p=1.0 tautology
- Do not assume delta 0.7143 vs 0.2857 fallback is meaningful — prior used fallback, current must compare same page type
- Do not assume synthetic Stagehand hit_rate 0.941 implies shipped 2x/30% transfers without drift MISS, random null, real latency/tokens
- Do not assume false_accept 0.0 without drift injection is safe — requires single-attribute mutation MISS test NC3
- Do not assume relaxed 0/16 on single-page implies pilot infeasible — requires multi-step rollouts
- Do not assume exhaustive CAP/LFS required — ABANDONED per Director; orthogonal narrow pilot only
- Do not assume Playwright 1.63.0 compatible with BrowserGym-core 0.14.3 — provenance shows 1.44.0; document pip freeze hash
- Do not assume cross-project isolation on 5 tests generalizes or that PC3 3-consecutive HIT was verified
- Do not assume within-store AX generalizes to cross-site — single Magento store only; cross-site needs multi-store dataset
- Do not re-use truncated-first-20 constant null F(n)=0.5654 as predictor

---

## 2. Hypotheses

**H1_AX_CONSISTENCY (confirmatory, primary):** Mean AX_consistency across 10 families (2 tasks each, longest-prefix without fallback, task-specific product pages at 1280x720) >=0.6 with bootstrap 95% CI lower >0.5, permutation p<0.05 vs NC1 family-label shuffle null, delta vs prior invalid 0.2857 >=0.20, and per-family variance >0 (not degenerate [1.0,1.0]), demonstrating identifiable same-mechanism parameterized transfer within WebArena-Verified v2 shopping. Discrimination vs prior inflated 0.9: report CI overlap and variance.

**H2_STAGEHAND_BASELINE (confirmatory):** Stagehand server-side selector+relevant-subtree SHA256 verb cache (exact normalized selector + relevant subtree outerHTML SHA256, HIT after N=2 identical results, per-project scope) replicated on >=30/36 families (drift test >=20) reports HIT on identical DOM >=0.8, MISS on single-attribute drifted DOM >=0.8, false_accept <0.05, beats NC4 random HIT/MISS null p<0.05, and reports measured cold vs cached latency/tokens via real dispatch path (not synthetic microsecond) vs B-RAG-EMBED-FLAT / B-SPIDER-0TOKEN / B-COLD-LLM bound, delivering shipped baseline comparison.

**H3_RELAXED_GATE0_CENSUS (descriptive, unblocking):** On same 20 captures plus multi-step BrowserGym trajectories (>=50 transitions per family, at least 10 families), relaxed Gate0 pass count (titles>=1, H(S_next|URL,H_K=3)>0.1 bits with >=5 per stratum, NL>=20, singleton<50%) and strict Gate0 pass count (titles>=2, H>0.2, NL>=50, strata>=10, leakage_validOnly<40%) reported with bootstrap CIs; >=1 relaxed pass suggests next physics can run correlated-state pilot H>0.1 without exhaustive search. Single-page NL=0 is unmeasured, not falsification.

---

## 3. State, action, target, observable

**State representation:** Raw CDP Accessibility.getFullAXTree nodes (role, name, value, properties) plus DOM outerHTML relevant-subtree SHA256 for Stagehand key (normalized). Title = document.title string; URL = normalized page URL (lowercase, strip query/fragment for leakage). For Gate0, H computed on state defined as (URL, H_K=3 history) if H needed for census (same as prior physics). No PCA/TF-IDF embedding for AX_consistency; longest-prefix operates on normalized selector patterns (tokenized selector path from AX node+DOM attributes).

**Action representation:** Element-pattern: normalized selector pattern derived from AX node + DOM attributes for target element (role+name+CSS path tokenized). Longest-prefix: longest common prefix of tokenized pattern (>0 tokens) across family tasks, no fallback to nearest-neighbour/TF-IDF/semantic.

**Target/observable:** Primary metric M-AX-CONSISTENCY = mean per-family indicator (1 if both tasks in family map to same longest-prefix pattern, else 0) across 10 families, range [0,1], with per-family variance reported. Secondary: M-STAGEHAND-HITRATE, M-STAGEHAND-MISSRATE, M-STAGEHAND-FALSE-ACCEPT, M-STAGEHAND-SPEEDUP, M-STAGEHAND-TOKENS-SAVED. Census: M-GATE0-RELAXED-PASS count/rate and M-GATE0-STRICT-PASS count/rate.

**Unit of analysis:** Family for H1 (n=10 families, 20 tasks, family-level bootstrap), per-family task for Stagehand (n=36 families, up to 72 tasks plus drift variants).

---

## 4. Sampling policy

- **Family sampling:** From 36 WebArena-Verified v2 shopping families with >=3 tasks (census 36 ge3), sample 10 families without replacement using seed 35725763380 (Python random, deterministic). Record ordered list; expect [136,208,211,172,191,139,138,222,101,194] if same sampling as parent, but recompute deterministically. Stratify not required; record artifact hash.
- **Task sampling:** Within each of the 10 families, sample 2 distinct tasks without replacement (seed 35725763380) prioritizing distinct start_url categories where possible (category, product detail, cart). Task IDs and expanded start_urls pinned in ax_captures.jsonl. Fixed placeholder expansion required for families with __SHOPPING__/path.
- **Stagehand replication:** Attempt all 36 families (>=30 required for H2 validity, >=20 for drift), sampling 2 tasks per family where possible (same families as H1 plus remaining 26); seed 35725763380 reused; report which families blocked.
- **Multi-step Gate0 rollouts:** For each of the 10 families, attempt BrowserGym rollout collecting >=50 transitions per family (click/type/navigate within shopping site); at least 10 families with multi-step required for census validity, else flag.
- **No CAP/Online-Mind2Web/Mind2Web LFS sampling this cycle** — explicitly ABANDONED per Director SUPERSEDE (no Mind2Web-2 long-horizon 130 tasks this pulse; that is intel's second step after this fix).

---

## 5. Holdout and contamination controls

- AX_consistency has no train/test split — it is within-family consistency of longest-prefix, no fitting on held-out families. No TF-IDF/k-means training to leak.
- Stagehand cache: keys fitted on first occurrence per (project_id, normalized_selector, relevant-subtree hash) and tested on second occurrence within same family (intra-family HIT test) and cross-project isolation test; no cross-family key reuse that would inflate hit_rate. Drift injection is single-attribute mutation on relevant subtree, not full-page.
- All 20 AX captures captured at 1280x720 initial viewport no scroll; below-fold or post-interaction AX after scroll/add-to-cart not included except via multi-step trajectory branch (which records post-interaction transitions for Gate0).
- BrowserGym/AgentLab/Playwright versions pinned and recorded; no post-hoc pin change after seeing AX scores. Placeholder fix verified by code hash before capture.

---

## 6. Nulls, baselines, and controls (stable IDs for EXECUTE/AUDIT)

**Baselines:**
- B-STAGEHAND-VERB (shipped Feb 2026 exact selector+relevant-subtree SHA256 2x/~30%, per-project) — H2 must match definition with drift test
- B-RAG-EMBED-FLAT (flat retrieval without DOM-hash guard) — hit vs false_accept comparison descriptively
- B-SPIDER-0TOKEN (verbatim 0-token replay) — token economics floor
- B-RANDOM-AX-SHUFFLE (1000 perms family-label shuffle) — null for H1 discrimination
- B-CONSTANT-NULL-05654 (REJECTED vacuous 0.5654) — disclosed only to prevent reuse
- B-COLD-LLM (cold agent from scratch, same model/tools/budget) — descriptive upper bound for honest economics, not executed as LLM inference

**Positive controls:**
- PC1_AX_LIVENESS_1280: >=15/20 AX trees 600-2000 nodes, DOM bytes >=2000, Docker reachable after 3 retries at http://localhost:7770
- PC2_AX_PRIOR_REPLICATION: >=1 family replicates prior 0.9 CI[0.7,1.0] longest-prefix but now on diverse product pages (variance>0 check)
- PC3_STAGEHAND_HIT_IDENTICAL: On stable family with 3 consecutive identical relevant-subtree hash+normalized selector, HIT on 2nd/3rd call with per-project isolation
- PC4_SYNTHETIC_PIPELINE: Synthetic validation retained but is_synthetic true, not decision input

**Null controls:**
- NC1_AX_SHUFFLE_NULL: 1000 family-label perms seed35725763380, true must exceed p95+0.30 with p<0.05
- NC2_AX_RANDOM_PATTERN: Random pattern from different family expected <0.2
- NC3_STAGEHAND_DOM_DRIFT: Single-attribute DOM mutation on relevant subtree expecting MISS; false_accept <0.05 and MISS>=0.8
- NC4_STAGEHAND_RANDOM_CACHE: Random HIT/MISS shuffling ~50% hit_rate ~1.0 speedup; true must beat p<0.05 (1000 perms)
- NC5_CROSS_PROJECT_LEAKAGE: Same key different project must MISS, cross-project HIT 0%

---

## 7. Primary metric and expected direction

**Primary confirmatory metric:** M-AX-CONSISTENCY (mean [0,1]) with bootstrap 95% CI and NC1 shuffle null, plus per-family variance and delta vs 0.2857.

**Expected direction under H1:** True >=0.6, CI lower >0.5, permutation p<0.05, delta >=0.20 above prior invalid 0.2857, variance>0 (not tautological), and discriminable vs single-family inflated 0.9 (CI width >0). If H1 holds, this is first measurement-valid within-store parameterized transfer on product pages.

**H2 primary:** M-STAGEHAND-HITRATE >=0.8 on identical, M-STAGEHAND-MISSRATE >=0.8 on drift, M-STAGEHAND-FALSE-ACCEPT <0.05, speedup and tokens_saved reported via real path, beats NC4 p<0.05.

No threshold changed after seeing outcomes. Longest-prefix without fallback only; placeholder expansion verified.

---

## 8. Uncertainty method and resampling unit

- Bootstrap 2000 percentile 95% CIs for M-AX-CONSISTENCY (resampling families, not tasks, to respect family-grouped dependency) and for Stagehand hit/miss rates (resampling families). Report lower, mean, upper.
- Permutation 1000 for NC1 shuffle null (permute family labels across 10 families, preserve per-family 2 tasks), seed 35725763380; report mean/std/p95 and permutation p = (1 + count perm >= true)/(1+1000). Same seed for NC4 random cache null (1000 perms shuffling HIT/MISS labels).
- All seeds deterministic; Python hash randomization not used (site pin via string compare). Resampling unit = family for AX, family/task for Stagehand. Family-level bootstrap for AX is required to avoid task-level independence violation (correlated transitions within family).

---

## 9. Adequacy and validity rules

**Adequate H1 run:** >=10 families (20 trees) with node counts 600-2000, viewport 1280x720, CDP hash recorded, longest-prefix without fallback verified by code hash, placeholder correctly expanded for __SHOPPING__/path families, per-family URL/title confirms product-page diversity; else MEASUREMENT_INVALID insufficient data (not FALSIFIED).

**Adequate H2 run:** >=30/36 families attempted with derived selector+relevant-subtree SHA256 cache logic (N=2, per-project), with >=20 families for drift injection and >=5 for cross-project isolation; else MEASUREMENT_INVALID.

**Adequate Gate0 census:** Multi-step trajectory with >=50 transitions per family for H/NL/strata; raw transitions per capture recorded even if <50, but H undefined if <5 per stratum flagged and excluded from H gate but still reported. Single-page capture alone cannot compute H/NL/strata => flag as descriptive viewport-only with 'unmeasured' and do not use to claim relaxed infeasible.

**Representation loss disclosed:** Longest-prefix pattern only (no semantic/subtree/multi-anchor), initial viewport no scroll for AX plus multi-step for Gate0, CDP AX vs full DOM, DOM-hash relevant-subtree outerHTML choice (normalized), N=2 HIT threshold, Playwright version deviation if 1.44.0 fallback.

---

## 10. Falsification / survival / invalidity rules (frozen, no post-hoc change)

```
IF Docker/CDP yields <5 families with task-specific product pages (<10 trees 600-2000 nodes) after 3 retries + placeholder fix verification:
  H1 = MEASUREMENT_INVALID substrate_unavailable (status COMPLETE outcome NOT_APPLICABLE)
  publish failure provenance, do not falsify, next pulse repair substrate
ELIF captured >=10 families (20 trees, placeholder expanded, longest-prefix verified):
  IF mean >=0.6 AND ci_lower >0.5 AND perm_p <0.05 AND delta_vs_0.2857 >=0.20 AND PC1 >=15/20 AND variance>0:
    H1 = SURVIVES (parameterized transfer identifiable at longest-prefix on product pages)
    discriminate vs prior 0.9: report CI overlap [0.7,1.0] and whether variance indicates inflated point estimate
  ELSE:
    H1 = FALSIFIED-IN-SETTING (bounded to WebArena v2 shopping longest-prefix on product pages)
    // variance=0 or p=1.0 despite diverse pages => FALSIFIED, not SURVIVES (homepage tautology bug not fixed)

IF Stagehand attempted <30/36 families due to Docker unavailability:
  H2 = MEASUREMENT_INVALID
ELIF attempted >=30 with derived selector+relevant-subtree SHA256:
  IF hit_on_identical >=0.8 AND miss_on_drift >=0.8 AND false_accept <0.05 AND speedup/tokens reported via real path AND beats NC4 p<0.05 AND PC3 isolation 0.0:
    H2 = SURVIVES (baseline replicable, competitive floor delivered)
  ELSE:
    H2 = FALSIFIED-IN-SETTING (selector+hash not discriminating on this shopping substrate)

H3 census descriptive (does not gate SURVIVES):
  Report relaxed_pass = count with titles>=1 & H>0.1 & NL>=20 & singleton<50 (multi-step)
  and strict_pass = count with titles>=2 & H>0.2 & NL>=50 & strata>=10 & leakage_validOnly<40%
  with bootstrap CIs; >=1 relaxed pass on multi-step suggests next physics relaxed pilot feasible
  0/16 on single-page alone = unmeasured not falsification

Overall SURVIVES if H1 SURVIVES and H2 at least reporting valid (preferred both SURVIVES);
H1 FALSIFIED alone suffices to reject this AX method for product within-store claim.
No CAP/LFS exhaustive search changes verdict; exhaustive remains ABANDONED.
```

All control/baseline/metrics IDs frozen for EXECUTE/AUDIT: B-STAGEHAND-VERB, B-RAG-EMBED-FLAT, B-SPIDER-0TOKEN, B-RANDOM-AX-SHUFFLE, B-CONSTANT-NULL-05654, B-COLD-LLM, PC1_AX_LIVENESS_1280, PC2_AX_PRIOR_REPLICATION, PC3_STAGEHAND_HIT_IDENTICAL, PC4_SYNTHETIC_PIPELINE, NC1_AX_SHUFFLE_NULL, NC2_AX_RANDOM_PATTERN, NC3_STAGEHAND_DOM_DRIFT, NC4_STAGEHAND_RANDOM_CACHE, NC5_CROSS_PROJECT_LEAKAGE, M-AX-CONSISTENCY, M-AX-CI-LOWER, M-AX-CI-UPPER, M-AX-SHUFFLE-P, M-AX-SHUFFLE-MEAN, M-AX-SHUFFLE-P95, M-AX-DELTA-VS-PRIOR, M-STAGEHAND-HITRATE, M-STAGEHAND-MISSRATE, M-STAGEHAND-SPEEDUP, M-STAGEHAND-TOKENS-SAVED, M-STAGEHAND-FALSE-ACCEPT, M-STAGEHAND-CROSS-PROJECT-LEAKAGE, M-GATE0-RELAXED-PASS, M-GATE0-STRICT-PASS.

---

## 11. Product consequence

**Positive (H1 SURVIVES + H2 reporting at least valid):** Delivers measurement-valid within-store parameterized transfer (10 families product pages, correct pins, longest-prefix >=0.6 discriminating) and shipped Stagehand baseline (hit>=0.8/miss>=0.8/false_accept<0.05 vs random, real latency/tokens, derived selector+subtree) — product can decide whether SPIDER parameterized inheritance beyond exact cache is justified and physics can run relaxed H>0.1 NL>=20 pilot on same families without inventing 4-point logistic/Hill extrapolation or 567.7MB LFS. Artifacts become reusable substrate for next physics/product holdout and Mind2Web-2 upgrade (second step after this fix, not substitute). C-CROSSSITE remains single-store so cross-site still HYPOTHESIS, but within-store family hold-out (C-LLM-INHERIT) advances toward VALIDATED.

**Negative (H1 FALSIFIED or H2 FALSIFIED or MEASUREMENT_INVALID):** If FALSIFIED, longest-prefix without fallback does not achieve identifiable transfer or Stagehand not discriminating on shopping product pages — product must try alternative pattern grammar (semantic/subtree/multi-anchor) or use RAG-EMBED/hierarchical retrieval, not assume within-store generalization; if MEASUREMENT_INVALID (<5 families with product pages after fix + 3 retries), no falsification, repair Docker/pins/placeholder and re-run orthogonal BrowserGym loopback or hierarchical retrieval, not exhaustive LFS/CAP. H2 FALSIFIED means Stagehand 2x/30% does not transfer to shopping families; product economics must use alternative baseline. H3 0 relaxed passes on multi-step keeps physics pilot blocked on shopping substrate. No exhaustive search re-triggered.

---

## 12. Cost and information

**Cost:** LOW-MEDIUM, no LLM API calls (token estimation via tiktoken if needed), Docker (~1-2GB) + BrowserGym-core 0.14.3 + AgentLab 0.4.2/0.3.0 + Playwright 1.63.0 Chromium (~300MB), 20 AX captures on product pages + Stagehand derived-key sweep (36 families) + multi-step rollouts (10x50 transitions) ~2.5-3.5h wall-clock, <12GB /tmp, stdlib+playwright+browsergym/agentlab. Reuses prior census d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30 for pin only.

**Information:** MAXIMUM per Director REOPEN comparative reasoning with cognitive_reset — directly repairs last-mile placeholder bug that caused degenerate homepage tautology (1.0 p=1.0) and synthetic Stagehand, with deterministic low-cost fix delivering discriminating AX test, spec-compliant baseline that determines SPIDER vs Stagehand economics, and relaxed Gate0 via multi-step that unlocks physics without exhaustive search. Either SURVIVES unlocks product within-store holdout and physics pilot, or FALSIFIED-IN-SETTING redirects to alternative representations and hierarchical retrieval, both decision-changing vs repeating stale exhaustive plan. Beats synthetic bandwidth tuning after 44-deep frontier tunnel and vacuous F=0.5654 extrapolation (closed).

---

## 13. Execution plan (frozen, no outcome inspection)

1. Pin and verify: pip install browsergym-core==0.14.3 agentlab==0.4.2 (fallback 0.3.0) playwright==1.63.0, playwright install --with-deps + chromium, record pip freeze sha256, verify CDP Accessibility.getFullAXTree, record versions.
2. Fix research/intel/exp_35789942386_measure.py:get_task_start_url to expand `__SHOPPING__/path` -> `http://localhost:7770/path` (base+path), verify via code hash and unit test on families 136/222 product paths, record hash.
3. Bring up Docker am1n3e/webarena-verified-shopping@sha256:3e8cb9b945 at http://localhost:7770, record digest, sample 10 families from 36 (>=3) seed35725763380, 2 tasks per family with task-specific expanded start_url (category/product/cart).
4. Capture 20 AX trees via CDP at 1280x720 initial no scroll (600-2000 nodes), compute AX_consistency longest-prefix without fallback (tokenized), bootstrap 2000 family-level, shuffle 1000 perms, report delta vs 0.2857 and vs 0.9 with per-family variance.
5. Replicate Stagehand selector+relevant-subtree SHA256 (N=2, per-project) on 36 families with derived normalized selector and relevant subtree outerHTML hash, inject single-attribute DOM drift on >=20 families, test cross-project isolation on >=5, report hit/miss/false_accept vs NC4 random null (1000 perms) and measured cold vs cached latency/tokens via real path vs B-RAG-EMBED-FLAT/B-SPIDER-0TOKEN.
6. Collect multi-step BrowserGym trajectories (>=50 transitions per family, 10 families) at 1280x720, compute relaxed vs strict Gate0 census (titles, H with >=5/stratum, NL, strata, leakage_validOnly, singleton) and preserve raw artifacts with sha256 + provenance; disclose representation loss; no CAP/LFS exhaustive search.

