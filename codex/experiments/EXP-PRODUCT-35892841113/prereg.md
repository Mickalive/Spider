# EXP-PRODUCT-35892841113 preregistration

**Lane:** product — Product economics / residual-novelty  
**Claims:** C-RESIDUAL-NOVELTY (primary, Director-mandated), C-PRODUCT-ECON (secondary, shared economics measurement)  
**Mode:** DESIGN (no outcome-bearing measurements inspected)  
**Director mandate:** CONTINUE C-RESIDUAL-NOVELTY — fixing kernel.resolve binding as minimal lever before PARK/pivot to WebMCP tool-bypass. SUPERSEDE active PREFREEZE EXP-PRODUCT-35891811410. Cognitive reset applied.  
**Parent handoff:** research/experiments/EXP-PRODUCT-35888533574/handoff.json (MEASUREMENT_INVALID bounded to binding bug) — used as continuity evidence only, does not override Director SUPERSEDE. Established/rejected/unknown/do_not_assume distinctions preserved below.

## 1. Scientific question

Director's strategic question (binding):
> Does fixing kernel.resolve parameter binding (so n=0 exact-repeat tasks correctly resolve with all required_slots present, hitting the 50-tok hit path instead of the 500-tok novel path) allow batched SPIDER with frontier correct-family reconstruction gating + TTL/ETag probe to achieve honest QCR per_hit <=0.85 vs RAG-EMBED at n0 and n0.25, <=1.20 vs Stagehand DOM-hash serverCache at n0, and <1.0 vs TERX 0-token replay at n>=0.25 with rho_novelty_per_hit>=0.60 |rho_length_per_hit|<0.20 under frozen bank same-ranker vary-only-post-retrieval QCR (Jaccard TAU0.30, 5000 family-stratified bootstrap + 5000 block-permutation |rho_shuffled|<0.20 p>=0.20 within-f std>0) on 192/36 WebArena-Verified v2 census (controlled novelty 0/25/50/75/100% train A test never-observed B) with verification-derived calibration false_accept<=0.10 UNKNOWN precision>=0.85 ECE<=0.15, reporting Pareto (tokens vs browser+latency vs accuracy) vs gpt-4o-mini+Playwright Docker 2000-node BrowserGym 1280x720 replication?

Converted to smallest rigorous falsifiable experiment: single-delta binding fix on otherwise identical 192/36 census, honest branch-derived cost at f=10, QCR frozen-bank same-ranker, batched MEA cache, TTL/ETag probe, frontier correct-family gating. If per_hit still >1.0 after fix, pay-novelty-not-length is rejected for this batched inheritance setting even with MEA/TTL/frontier wired.

## 2. Hypothesis

Fixing the single diagnosed root cause from EXP-PRODUCT-35888533574 (VF-PC2-BINDING-CRITICAL: confidence 0.5 < min_confidence 0.8 blocks EXECUTABLE even when required_slots satisfied, plus literal action_template body {} without placeholder slots) — by promoting distill confidence to >=0.80 after verified curation, inducing action_template placeholders via distill_parameterized `_template_slots` (e.g., `${body.sku}`, `${store_id}`, `${variant}`) consistent with `src/spider/kernel.py:_bind`, and generalizing preconditions to family+intent only so that `required_slots = parameter_slots ∪ _template_slots(action_template)` are fully present at resolve — will restore `P-SPIDER-MEA-BATCHED` `binding_correctness_n0=1.0` and `executable_rate_n0=1.0` on the 36 n=0 exact-repeat tasks, moving those tasks from the 500-tok novel path (parent observed 512.13 per_hit) to the 50-tok hit path.

While preserving batched MEA auditor caching (effectiveFetchAvg ~28 tok, cacheHitRate ~0.81, blockRate 1.0 on both miss and hit), TTL/ETag probe discrimination (accuracy>=0.90, saving>=30%, falseAccept<0.05), and frontier correct-family gating (crossFamilyAdoption=0), the fixed SUT will then achieve honest per_hit <=0.85 vs RAG-EMBED at n0 and n0.25, <=1.20 vs Stagehand at n0, <1.0 vs TERX at every n>=0.25, with residual-novelty tracking `rho_novelty_per_hit>=0.60` and `|rho_length_per_hit|<0.20` (family-stratified bootstrap 5000 + block-permutation 5000), and verification-derived calibration `false_accept<=0.10 UNKNOWN_precision>=0.85 ECE_exec<=0.15`.

## 3. State representation

- File-based synthetic WebArena-Verified v2 proxy 192 tasks /36 families /49 templates /duplication 0.9479 /param_task 0.8958 /L 8-14 family-specific slots `${sku},${store_id},${variant},${category}` via actual `src/spider/kernel.py:distill_parameterized` Jaccard>=0.55-0.75 constant-anchor field-path `body.*|headers.*|url`.
- Mechanism: `mechanism_id`, `intent`, `preconditions` (family+intent after fix), `action_template` (with induced placeholders), `postconditions`, `parameter_slots`, `confidence>=0.80`, `evidence` hashes.
- Fresh-context LLM flag: context truncated at 25k tokens, retrieval injected at 25k boundary with provenance graph.
- TTL state: `ttl_created`, `current_time`, `ttl_seconds=60`, `ETag W/body_sha`, `If-None-Match`, `probeHit/etagMatched/ttlValid/probeLatencyMs`, `cacheHit`.
- Frontier adapter state: `family_id` keyed, Jaccard>=0.30 in-family only, crossFamilyAdoption counter.
- Verification state: `verified_state` hash, `auditorBlocked` flag, provenance hash chain.

## 4. Action representation

Registry `MechanismRegistry` via `src/spider/kernel.py:_bind` and `resolve()`. Actions: `observe`, `distill` (parameterized with slot induction), `resolve(intent, context, params)`, `verify(mechanism_id, observed_state)`, `invalidate`. Distill promotes only after `verify(verified_state)` passes. Bind uses `_PARAMETER` regex `\$\{([A-Za-z_][A-Za-z0-9_]*)\}` and `_template_slots` / `_bind` full-match semantics. Frontier reconstruction is in-family state-conditioned lookup (cost 50 tok) gated by family_id and Jaccard threshold, not cross-family.

## 5. Target / primary metric

Primary discriminant: `M_per_hit = (M_total_f10 - retrieval - distill_amort - auditor_amort)/L` (honest kernel-gated branch-derived cost per step, excluding fixed overhead per Director). Secondary: `M_total_f10`. Both reported.

Primary statistical target: Spearman `rho_novelty_per_hit` (M_per_hit vs controlled novelty n) and `rho_length_per_hit` (M_per_hit vs task length L) pooled N~192, family-stratified. Supporting: per_hit parity ratios `SPIDER/RAG at n0`, `SPIDER/RAG at n0.25`, `SPIDER/Stagehand at n0`, `SPIDER/TERX at n>=0.25` (four levels 0.25/0.5/0.75/1.0), R2_delta per_hit (novelty vs length), calibration `false_accept`, `UNKNOWN_precision`, `ECE_exec` 5-bin, `confidence_std`.

Units: tokens (LLM), browser_calls, latency_ms (probe vs fullVerify).

## 6. Sampling policy

WebArena-Verified v2 census 192/36: per-family disjoint Curated-A (train) / B (test never-observed) pools zero overlap, frozen bank TFIDF Jaccard TAU0.30 same ranker for all retrievers (qcr_bank_manifest.json). Fractions n ∈ {0, 0.25, 0.50, 0.75, 1.00} realized by sampling test tasks where n fraction of parameterizable slots drawn from B and (1-n) from Curated-A stratified by slot position header vs url and family, orthogonal to L (8-14 constant within family). n=0 exact-repeat sequences so TERX/Stagehand hitRate 1.0 reachable. Train 5 demos/family on Curated-A only, one Mechanism/family via actual distill. Batched cache fit on Curated-A only. Frontier adapter correct-family gating in-family only. All fit on TRAIN only. Realized novelty disclosed per task. If /tmp/webarena or repo-cached JSON present, load; else generate synthetic family-structured mock exactly replicating 36/49 ratios and log provenance, disclose ceiling synthetic file-based not Docker/full-DOM.

No outcome-bearing measurement before freeze; freeze.json hashes request/spec/prereg + code hashes before result.json.

## 7. Unit of analysis / holdout

Unit: per-task M_per_hit and per-step branch trace. Holdout: within-family controlled novelty — train on Curated-A, test on B never-observed identifiers (honest parameterization test, not same-identifier replay). Novelty fractions are the independent variable, not a random train/test split leakage. Family is the resampling unit for bootstrap/block-permutation (resample families with replacement then tasks within, respecting dependency structure; |rho_shuffled|<0.20 test uses family-label permutation). QCR frozen bank ensures vary-only-post-retrieval: same ranker, same retrieval candidates, only post-retrieval support (hit vs novel vs repair vs probe) varies.

## 8. Baselines (strong, same 192-task family-stratified splits, honest accounting, QCR same ranker)

- **B-COLD** (cold start): novel 500+2 calls per step + 50+120ms verify, no retrieval/auditor/probe/reconstruction. Flat vs n expected ~500 per_hit. Denominator.
- **B-RAG-EMBED** (RAG semantic retrieval): frozen bank 36 families Curated-A, TFIDF Jaccard TAU0.30 identical ranker, top-1 verbatim bind with verify fallback to COLD. Honestly retrievable at n=0 and proportionally at n=0.25. Post-retrieval verbatim only. Expected ~54.7 at n0 -> ~504.7 at n1; SUT must beat >=15% at n0 and n0.25.
- **B-STAGEHAND-CACHE** (Stagehand DOM-hash serverCache): exact-selector + DOM-hash 2000 nodes 1280x720 CDP AX hash ~48h TTL, hit iff DOM identical (n=0) else COLD. Honest 50+120ms hit. Hit_rate 1.0 at n0, 0 at n>=0.25. Shipped 80% speedup baseline.
- **B-TERX-REPLAY** (TERX/BrowserBash 0-token replay+LLM fallback): if identifier sequence exactly equals training trajectory (n=0) replay at 0 LLM tokens +50 verify +1 call else COLD. Honest 50 verify. HitRate 1.0 at n0, 0 at n>=0.25. Must be beaten <1.0 at every n>=0.25.
- **P-SPIDER-MEA-BATCHED** (SUT with binding fix): curated exploration (5 demos/family, confidence>=0.80, template placeholders via _template_slots) + MEA auditor batched caching (first per family 100+80ms miss, hits 10+15ms, provenance hash chain, context truncation 25k, blockRate 1.0 even on hit) + TTL/ETag probe (10+30ms conditional HEAD with ETag W/body_sha If-None-Match TTL 60s max_age via deterministic map seeded 42 ~50% stale exercising ETag mismatch, fallback 50+120ms) + frontier validated state-conditioned reconstruction adapter with correct-family gating (family_id + Jaccard>=0.30 in-family only, crossFamilyAdoption must be 0, cost 50 tok) + freshness gating 0.25 + softmax temp0.15+jitter UNKNOWN<0.80 + verify+repair 500+2 on fail fallback to COLD on UNKNOWN. Amortized distill 1000/f + auditor 100/f (f=10) only SUT. Genuine branch-derived sums.

All per_hit excludes retrieval/distill/auditor for parity; total includes them. None starved; hitRate n=0 must be 1.0 inside compared set.

## 9. Positive / null controls and validity threats

**Positive control PC-MEA-BATCHED-TTL-CACHE (stable id):**

- PC1 Exact-repeat cache: B-TERX and B-STAGEHAND at n=0 must achieve hit_rate 1.0, 50 tok verify-only per_hit, success 1.0.
- PC2 Binding+governance with FIX (critical for this experiment): P-SPIDER-MEA-BATCHED curated on 5 demos/family must resolve EXECUTABLE with correct bound_action via actual `src/spider/kernel.py:_bind` on held Curated-A at n=0 — `binding_correctness_n0=1.0` `executable_rate_n0=1.0` (5/5 per-family spot-check family-stratified), confidence >=0.80, action_template contains induced placeholders via `_template_slots`, AND auditor blocks 100% unverified writes on both cache-miss and cache-hit paths (blockRate 1.0, provenance chain with cacheHit flag, cacheHitRate 0.75-0.85, effectiveFetchAvg ~28 tok). This is the gate that failed parent (0.0/0.0, confidence 0.5, literal body {}).
- PC3 TTL/ETag probe discrimination: on deterministic map seeded 42 ~50% fresh/~50% stale, probe must discriminate fresh (TTL valid + ETag match -> 10 tok hit) vs stale (expired/mismatch -> 50 tok fallback) with accuracy>=0.90 latency saving>=30% vs full verify and probeFalseAccept<0.05, both paths logged per-step.
- PC4 Non-vacuous verification: forced-execute wrong-bound mock with shuffled adapter must yield false_accept in [0.10,0.60] and success<=0.90, and batched cache must still enforce verify on shuffled hash (no cache bypass).

Failure of any PC -> MEASUREMENT_INVALID irrespective of economics, not falsification. PC2 is the binding-fix gate for this experiment.

**Null controls NC-MEA-BATCHED-SHUFFLE (stable id):**

- NC1 Shuffled auditor+adapter+cache: permute parameter_slots + swap verified_state hash + swap frontier keys + randomize cacheHit before resolve via actual pipeline; mock wrong-bound p=0.15, auditor should reject even on hit -> UNKNOWN, frontier cross-family -> UNKNOWN. Expect `|rho_novelty_per_hit|<0.25` p>=0.05, `|rho_shuffled|<0.20` p>=0.20 per mandate, success<=COLD, false_accept 0.10-0.60 if forced, UNKNOWN>=0.80, crossFamilyAdoption 0, within-family std>0, cache does not inflate success.
- NC2 Random mechanism+probe+adapter+cache: random registry/probe/adapter/cache, expect false_accept>=0.10 or |rho|<0.25 and success<=0.90.
- NC3 Length-proportional fail-able: cost = L*500 constant per_hit 500 regardless novelty, expect |rho|<0.25 R2<0.15 on both total and per_hit proving environment can express MIXED/FALSIFIED.
- NC4 Ablation: MEA no-auditor vs MEA, uncurated vs curated, adapter off vs on, batched off (100 tok fixed) vs batched, must show causal deltas (without auditor false_accept>0.20, without curated success drop>0.10, without adapter per_hit worsens, without batched per_hit worsens >10% at n0) otherwise mechanism not causal.

If NC1 shows `rho>=0.35` p<0.01 -> MEASUREMENT_INVALID (novelty confounded or bypass).

**Validity threats disclosed:**

- Frontier char-bigram Jaccard A/B pools share bigrams by construction yielding Jaccard>=0.7 and 100% hitRate at n=1.0 tautology in parent; parent's TERX-beating was artifact. This design requires orthogonal alias families or discloses that frontier 1.0 hitRate at n=1.0 is tautological; per_hit vs TERX must not be claimed if frontier hitRate=1.0 due to construction.
- TTL/ETag deterministic map seeded 42 is independent of novelty; expected fresh at n0 is ~1.0 on real CDN but map yields ~0.53 random, so probe hitRate 0.531 at n0 and 39.8% saving are not CDN freshness validation.
- File-based synthetic proxy ceiling: 192/36 file mock not Docker full-DOM 2000-node BrowserGym 1280x720 or real gpt-4o-mini token economics; rho_proxy_real unmeasured until Docker replication.
- Confidence calibration degeneracy: parent had confidence_std 0.0125 due to all-UNKNOWN collapse (EXEC n=0), ECE 0.783 with 4/5 empty bins; this experiment must achieve mixed EXEC/UNKNOWN to measure calibration non-vacuously.
- Batched cache decoupling: cacheHit must not bypass verification; NC1 exercises this on both paths.

## 10. Primary metric, expected direction, uncertainty

- Primary: per_hit parity ratios `SPIDER/RAG at n0`, `SPIDER/RAG at n0.25` (both <=0.85 required), `SPIDER/Stagehand at n0` (<=1.20), `SPIDER/TERX at n>=0.25` four levels (each <1.0).
- Correlation: `rho_novelty_per_hit` >=0.60 (positive: cost rises with novelty), `|rho_length_per_hit|<0.20` (length not primary driver), `R2_delta per_hit>0.10`, `|rho_shuffled|<0.20` p>=0.20, within-f std>0.
- Calibration: `false_accept<=0.10`, `UNKNOWN_precision>=0.85`, `ECE_exec<=0.15` (5-bin derived, confidence_std>0.05, 3 empty bins disclosed), verification-derived with MockEnv wrong-bound p=0.15 non-vacuous.
- Governance: probe accuracy>=0.90 saving>=30% falseAccept<0.05, auditor blockRate 1.0 on both paths, cacheHitRate 0.75-0.85 effectiveFetch ~28 tok, frontier crossFamily 0.

Uncertainty: family-stratified bootstrap 5000 (resample families with replacement then tasks within) for 95% CIs on rho, R2_delta, ratios, probe saving, auditor precision, frontierHitRate, cacheHitRate, curatedDelta; block-permutation 5000 (family-label permutation) primary p for rho and ratio differences; heteroscedasticity-robust SE for regressions; Wilson 95% for rates; degenerate CI [1,1] flagged degenerate not precision; ANOVA novelty×length if p<0.05 disclose within-stratum rho_length.

Expected direction: with binding fix, SUT per_hit at n0 ~50-70 (vs RAG 54.7 -> ratio ~0.85-1.0), at n0.25 ~180 vs RAG ~208 -> ratio ~0.85, rho 0.60-0.80, |rho_length| <0.20. Without fix, parent showed 9.35 at n0.

## 11. Adequacy rule

Power >0.95 to detect per_hit ratio <=0.85 vs 1.0 at N=192 family-stratified pooled; satisfied per prior power note. Minimum N=192/36 families. Require PC1-PC4 pass and NC1-NC4 discriminating (not degenerate) and at least 5% UNKNOWN exercised at n=1.0 (governance exercised). If PC2 still fails (binding_correctness <1.0), measurement invalid regardless of other metrics.

## 12. Falsification / survival rule

Compute per-method success, false_accept, UNKNOWN_precision, ECE_exec 5-bin, M_total_f10, M_per_hit per task, Spearman rho_novelty_per_hit (primary), rho_total, rho_length_per_hit, R2, parity ratios with bootstrap CIs, probe/auditor/frontier/cache metrics, curated delta, NC1 rho_shuffled, within-f std, Pareto tokens/browser/latency/probe/auditor/cache/frontier split.

**SURVIVES_CURRENT_TEST iff ALL hold:**

- (C1) correctness+calibration: success at n0 >=0.85 (Wilson lower>=0.72), mean success >=0.80, false_accept<=0.10, UNKNOWN_precision>=0.85, ECE_exec<=0.15 (confidence std>0.05, PC4 non-vacuous verified).
- (C2) positive controls: PC1 hitRate 1.0 per_hit 50 tok success 1.0; PC2 binding 5/5 per family 1.0 via _bind with confidence>=0.80 and template slots present AND auditor 1.0 blockRate on both miss and hit with cacheHit flag; PC3 probe accuracy>=0.90 saving>=30% falseAccept<0.05 with ~50% stale both paths logged; PC4 false_accept in [0.10,0.60] — any failure -> MEASUREMENT_INVALID.
- (C3) pivot per_hit economics: <=0.85 vs RAG at n0 AND n0.25, <=1.20 vs Stagehand at n0, <1.0 vs TERX at every n>=0.25 (family-stratified bootstrap CIs).
- (C4) residual-novelty correlation: rho_novelty_per_hit>=0.60 (p<0.01, CI lower >=0.40) and |rho_length|<0.20 (CI upper <0.30) pooled, R2_delta>0.10, NC1 |rho_shuffled|<0.20 p>=0.20 within-f std>0.
- (C5) governance invariants: probe accuracy/saving/falseAccept, auditor 1.0, frontier crossFamily 0, curatedDelta>0.10.
- (C6) Pareto reported (tokens vs browser+latency vs accuracy, decomposed).

If C3 fails but C4 passes -> MIXED; if C4 fails but C3 passes -> MIXED. **FALSIFIED** if C3 or C4 fail with C2 passing.

**MEASUREMENT_INVALID** if any PC fails or bijective formula detected or registry never consulted or UNKNOWN never exercised or frontier 1.0 artifact dominates or NC1 confounded. Precedence: PC failure > FALSIFIED (per frozen rule, consistent with parent audit precedence).

Docker full-DOM 2000-node BrowserGym 1280x720 with real gpt-4o-mini tokens/browser_calls is exploratory if available: replicate subset with Playwright 1280x720 CDP AX tree hash, 15-step budget temp0 seed42, report Pareto alongside proxy with rho_proxy_real correlation; if substrate unavailable or health check <80% AX>10 nodes, disclose as not executed, retain proxy-only conclusion bounded to file mock, log failure.json with smallest next action (runtime distributed-store+BrowserGym repair). Does not gate SURVIVES but informs promotion readiness.

## 13. Product consequences

- **Positive (SURVIVES):** C-RESIDUAL-NOVELTY advances HYPOTHESIS->EXPERIMENTAL bounded to WebArena-Verified v2 file-based census 192/36 proxy with binding-fixed curated exploration + MEA batched caching (fresh-context 25k + external verified_state batched ~28 tok avg) + TTL/ETag probe + frontier correct-family gating (TAU0.30) under QCR same-ranker and honest kernel-gated cost f=10 with verified novelty-proportional correlation. First non-parameterization evidence that governed-memory + cheap verification + correct-family reconstruction + batched caching achieves honest-cost targets falsified at 1.0-1.57 vs RAG and 1.61 vs Stagehand and that parent 9.35 was purely binding artifact. Unblocks C-PRODUCT-ECON amortized interpretation via validation+reconstruction and C-FRESHNESS via TTL/ETag selective invalidation. Justifies promoting MEA batched harness+TTL probe+frontier adapter as product lever vs selector cache despite Stagehand 80% speedup at exact repeat, using per_hit ratios/probeSaving/cacheHitRate/frontierHitRate as pricing prior and Pareto. No PRODUCT_CORE promotion without Docker full-DOM + HS256 distributed-store replication and rho_proxy_real >=0.50.

- **Negative (FALSIFIED with controls PASS):** Governed-memory batched pivot as implemented does not yield residual-novelty-proportional compression vs retrievable RAG or shipped Stagehand cache on this census; either batched 28 tok avg +100 distill +10 auditor +50 frontier -40 probe =148 tok fixed overhead still dominates at n0 despite hitting 50-tok path, or frontier orthogonal families not improving beyond RAG, or rho flatness persists (cost not tracking novelty). Product must NOT claim pay-cost-of-novelty for C-RESIDUAL-NOVELTY/C-PRODUCT-ECON via this harness+adapter on this setting; acknowledge Stagehand dominance at exact repeat and RAG at n0.25 remains strong baseline where SPIDER fails. This is last discriminating test before PARKing residual-novelty and pivoting Product to WebMCP tool-bypass compilation (714 sites 2147 tools, O(1) tool discovery vs O(M×N) browsing) as primary economics lever per Scout, as stated in Director comparative reasoning. Bounded REJECTED for MEA-batched+TTL+frontier proxy setting only, not global falsification (may transfer with orthogonal alias families, richer DOM/QCR post-retrieval, f=100 amortization, or distributed HS256 substrate). No promotion; Pareto shows where cost accumulates. If MIXED, keep HYPOTHESIS and investigate overhead dominance vs per_hit isolation. If MEASUREMENT_INVALID due to PC2 still failing, binding fix insufficient -> require kernel preconditions/template re-fix before any economics claim.

## 14. Estimated cost

Low-moderate file-based primary: 192 tasks ×3? Actually 192 tasks ×5 conditions (COLD/RAG/Stagehand/TERX/SPIDER-MEA-BATCHED) +4 null controls (~768) = ~1728 deterministic resolve/_bind/MEA-batched-verify/TTL_probe/frontierAdapter trials plus curated vs uncurated + MEA no-auditor + frontier off + cache on vs off ablations (~768) plus TFIDF offline and MockEnv p=0.15 branches plus batched cache hit/miss tracking. Wall <60min CPU proxy (<100min if Playwright 2000-node 1280x720 loopback exercised with gunicorn+nginx). Storage per-task CSV ~2700 rows, registry JSONL, cost_config, branch_traces with probe/auditor/cacheHit/frontier flags, probe_traces, curated_manifest, qcr_bank_manifest, frontier_adapter traces, provenance. If Docker+gpt-4o-mini exploratory: 192×5×~15 steps Playwright ~3000 calls ~2000 gpt-4o-mini calls <$15 plus BrowserGym snapshot storage. No LLM keys required for proxy decision; ~$12-15 if real LLM exploratory.

## 15. Expected information gain

Very high and decisive per Director rationale: directly tests the single remaining lever from EXP-PRODUCT-35888533574 audit PASS diagnosis (n0 binding bug inflating per_hit to 9.35). Fixing kernel.resolve confidence+template+preconditions is a single-line kernel change with decisive falsifier: if per_hit still >1.0 vs RAG/Stagehand after hitting 50-tok path at n0, then pay-novelty-not-length is rejected for parameterized/batched inheritance at freshness 0.25 even with MEA auditor and TTL probe already wired to block 100% unverified writes. If it achieves targets (<=0.85 vs RAG at n0/n0.25, <=1.20 vs Stagehand at n0, <1.0 vs TERX at n>=0.25 with rho>=0.60), it reopens honest saving >=25% vs COLD and validates batched governance before PARKing. Prior 28+ product experiments never met honest f=10 per_hit targets on file mock (prior honest 1.0 at n0 1.57 at n0.25, Stagehand 1.61 remain falsified until fix). Either valid positive or valid negative definitively decides Product architecture: continue batched mechanism distillation vs selector cache vs WebMCP tool-bypass compilation, providing DolphinBench-style Pareto and rho_proxy_real for commercial viability without another MEASUREMENT_INVALID loop. Dependencies: graph kernel distill fix determines required_slots for n0 hit, frontier correct-family gating adapter from EXP-FRONTIER-35793584484, runtime TTL/ETag probe shared WAL not required for census-level measurement.

## 16. Inherited state (from handoff EXP-PRODUCT-35888533574)

**Established (preserve):**
- Batched MEA auditor caching works: 0.8125 hitRate (156/192) effectiveFetch 26.875 tok (artifacts/cache_traces.json)
- TTL/ETag probe discrimination works: accuracy 1.0 saving 39.8% falseAccept 0 probe_traces.json
- Frontier correct-family gating works: hitRate_correct 1.0 crossFamily 0 frontier_adapter_traces.json
- Auditor governance works: blockRate 1.0 on both paths, 25k truncation, provenance hash chain
- Honest kernel-gated branch-derived cost accounting verified (no n*3200 formula)
- Strong baselines correctly implemented not starved under QCR TAU0.30
- Null controls discriminating and non-vacuous

**Rejected (bounded to that binding+confidence+literal-template+census):**
- Batched MEA at f=10 with current binding does NOT achieve per_hit <=0.85 vs RAG at n0 (9.35) or n0.25 (2.42) nor vs Stagehand (9.35) — not global C-RESIDUAL-NOVELTY falsification due to MEASUREMENT_INVALID precedence.

**Unknown (this experiment resolves first):**
- Whether fixing confidence+template+preconditions restores binding 5/5 per family and executable_rate 1.0 at n0 reducing per_hit to ~50-70 and achieving <=0.85.
- Whether rho becomes >=0.60 |rho_length|<0.20 once hit path reachable and frontier <1.0 at high novelty.
- Whether frontier orthogonal families yields realistic 0.3-0.6 at n=1.0.
- Whether calibration achieves std>0.05 UNKNOWN_precision>=0.85 ECE<=0.15 with mixed EXEC/UNKNOWN.
- Whether proxy per_hit correlates with real Docker gpt-4o-mini Pareto (rho_proxy_real).

**Do not assume (guard):**
- Batched cache not broken; per_hit 9.35 was novel path not cache overhead.
- rho -0.447 was artifact (frontier 1.0 + invalid n0) not valid novelty tracking.
- MEASUREMENT_INVALID != global FALSIFIED; claims remain HYPOTHESIS per Codex.
- Probe 0.531 hitRate and saving not CDN validation (deterministic map independent of novelty).
- File synthetic ceiling does not transfer to Docker full-DOM without measurement.

---

*Preregistered 2026-09-23 — no outcome-bearing measurements inspected. Frozen hashes in freeze.json will precede result.json.*
