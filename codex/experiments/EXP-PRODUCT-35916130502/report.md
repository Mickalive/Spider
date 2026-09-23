# EXP-PRODUCT-35916130502 — Report (Product Lane PIVOT)

**Experiment:** EXP-PRODUCT-35916130502 — Stagehand selector-cache + TTL 60s freshness gating vs WebMCP Registry 714/2147 O(1) on WebArena-Verified v2 192/36 orthogonal alias families at honest f=10 (frozen-bank QCR same-ranker vary-only-post-retrieval)

**Lane:** product — `src/spider/kernel.py` + `tests/` + `sdk/` (binding `director_mandate PIVOT` with cognitive_reset, SUPERSEDE disposition on parent EXP-PRODUCT-35908252617)

**Claims:** `C-PRODUCT-ECON` (primary) + `C-RESIDUAL-NOVELTY` (paired work-compression) + `C-FRESHNESS` (TTL/ETag)

**Status:** `COMPLETE` — `FALSIFIES` (valid negative, not infrastructure failure)

## Question & Hypothesis

**Frozen question (spec.json):** On 192/36 orthogonal alias families (Jaccard <0.30, disjoint alphabets, L=8-14) with controlled novelty 0/25/50/75/100% (Curated-A / never-observed B) under frozen-bank QCR same-ranker (TFIDF Jaccard TAU0.30 top-1), does Stagehand selector-cache + TTL 60s conditional probe (10 tok+30ms vs 50+120ms, ~50% stale via seeded 42 map) at honest f=10 achieve per_hit <=0.85 vs RAG-EMBED at n0 and n0.25 and <=1.20 vs Stagehand DOM-hash HIT at n0 with |rho_shuffled|<0.20 and Pareto tokens vs browser+latency vs accuracy, and does WebMCP 714/2147 O(1) survive only at f=100 or Docker rho_proxy_real>=0.5?

**Hypothesis (falsifiable):** Stagehand selector-cache + TTL has strictly higher leverage than parameterization or WebMCP O(1) at honest f=10 because it replaces 200 tok+150ms retrieval with 10 tok+30ms probe (no distill 1000/f or compile 800/f) on orthogonal families where RAG is only proportionally retrievable and Stagehand without TTL hits only at n0. Expected: probe accuracy>=0.90 saving>=30% falseAccept<0.05 ~50% stale, per_hit <=0.85 vs RAG at both n0 and n0.25 (both required, bootstrap CI must clear), <=1.20 vs StagehandCache at n0, calibration intact, Pareto dominance on M_total_f10.

## Design (frozen, summary)

- **Census:** 192 tasks /36 families, 49 templates, duplication 0.9479, L=8-14 family-specific slots `${sku},${store_id},${variant},${category}` via `kernel distill_parameterized` single-prefix induction, **orthogonal repair** A/B pools disjoint alphabets per family, cross-family bigram Jaccard 0.0 <0.30 verified 630 pairs, hitRate at n1.0 0.387 in 0.3-0.6 (not 1.0 tautology), train 5 demos/family from Curated-A only.
- **Binding fix:** `kernel.py _PARAMETER` dot-regex `r'\$\{([A-Za-z_][A-Za-z0-9_\.]*)\}'` re-applied (patched sha d926279d), confidence>=0.80, 5/5 per-family spot-check 36/36 EXECUTABLE via kernel.resolve.
- **Baselines (identical 192 splits, honest costs):** `B-COLD` 500 tok+2 calls per step; `B-RAG-EMBED` 200+150ms top-1; `B-STAGEHAND-CACHE` DOM-hash 50+120 1 call hit iff n0; `B-TERX-REPLAY` 0-token exact replay 50 tok at n0 else COLD; all frozen-bank same ranker.
- **Primary SUT `P-STAGEHAND-TTL`:** DOM-hash selector cache (2000-node 1280x720 hash) + TTL 60s conditional probe (10+30 HEAD If-None-Match W/body_sha vs 50+120 fullVerify via seeded 42 map ~50% stale both paths logged) + verification-derived calibration (softmax temp0.15 jitter, UNKNOWN when confidence<0.80 or freshness<0.25 or probe stale, MockEnv wrong-bound p=0.15). No distill/compile/auditor overhead; honest per_hit = M_total/L (probe stays inside).
- **Secondary `P-WEBMCP-TOOL`:** 714 sites 2147 tools O(1) hash lookup 15+10ms + compile 800/f (f=10 and f=100) + same TTL probe + frontier correct-family gating 50 tok crossFamily 0; honest per_hit = (M_total - tool_lookup - compile - auditor)/L.
- **Contrast `P-SPIDER-MEA-BATCHED`:** curated batched MEA 1000/f + auditor batched 10 hit/100 miss effective ~28 tok, frontier TAU0.30, TRAIN-warmed only.
- **Controls:** PC1-PC5 PASS required else MEASUREMENT_INVALID; NC1-NC4 via actual pipeline.

## Results (RAW -> OBSERVATION -> DERIVED)

### Positive controls — PASS non-degenerate

- **PC1 Exact-repeat:** B-TERX hitRate 1.0 (36/36), B-STAGEHAND hitRate 1.0 (36/36), per_hit 54.7 honest 50-tok verify, success 1.0 — PASS.
- **PC2 Orthogonal + binding + registry:** cross-family max Jaccard 0.0 <0.30 (0/630), hitRate_n1 0.386 in 0.3-0.6 (not tautology), kernel binding 1.0/1.0 confidence 0.85 via 5/5 spot-check EXECUTABLE, WebMCP registry 714/2147 count+hash verified, toolHitRate_n0 1.0 via actual lookup 15 tok (5/5 spot-check), SPIDER cacheHitRate 0.895 TRAIN-warmed effective 20.65 tok, auditor blockRate 1.0 both paths — PASS.
- **PC3 Probe:** accuracy 1.0 (>=0.90), saving 0.328 (>=30%), falseAccept 0.0 (<0.05), probeHit 0.505 (Stagehand) /0.422 (WebMCP) 97/192 and 81/192, ttl_valid 0.60/0.49, both paths exercised ~50% stale seeded 42 — PASS.
- **PC4 Non-vacuous:** NC2 false_accept 0.151 in [0.10,0.60] via actual pipeline 60% forced wrong — PASS proving mock can fail.
- **PC5 Honest cost:** frozen formula recomputed within 4.5e-7 (probe 10 vs retrieval 200 vs tool 15 honored, no n*3200, no frontier/probe exclusion, TRAIN-warmed only, frontier not 1.0) — PASS.

No PC failure => not MEASUREMENT_INVALID on PC gate.

### Primary economics — StagehandTTL FALSIFIES at n0

- **Per-hit means (L-normalized, honest f=10):**
  - RAG: n0 54.748, n0.25 208.030, n0.5 363.770, n0.75 458.011, n1 504.766
  - StagehandTTL: n0 57.206, n0.25 57.796, n0.5 160.199, n0.75 253.241, n1 286.370
  - StageCache: n0 54.748, n>=0.25 504.7
  - WebMCP: n0 56.508, n0.25 63.964, n0.5 77.176, n0.75 82.389, n1 86.931

- **Ratios (family-stratified bootstrap 95% CI):**
  - **StagehandTTL / RAG n0:** 1.045 CI [1.034,1.056] >0.85 — **FAILS F1-TTL** (requires ≤0.85 at *both* n0 and n0.25, CI must clear). Block-permutation p<0.01 for difference but in wrong direction (Stagehand worse).
  - **StagehandTTL / RAG n0.25:** 0.278 CI [0.249,0.339] ≤0.85 passes, but both required => F1 fails.
  - **StagehandTTL / StageCache n0:** 1.045 ≤1.20 — passes F2-TTL (parity within 20% probe overhead).
  - **StagehandTTL / TERX:** n0.25 0.114 (<1.0), n0.5 0.317 (<1.0), n0.75 0.502 (<1.0), n1 0.567 (<1.0) — all pass.

- **Residual novelty:** Stagehand rho_novelty_per_hit 0.472 CI [0.31,0.61] <0.60 target (descriptive, not gating but reported); pooled |rho_length| 0.306 >0.20, per-stratum up to 0.476 indicates length confounding.

- **WebMCP secondary reproduction:** WebMCP/RAG n0 1.032 CI [0.96,1.12] >0.85 fails (reproduces EXP-PRODUCT-35908252617 falsification 1.005>0.85), n0.25 0.307 passes but both required => fails at f=10. At f=100 exploratory per_hit 48.2/54.7=0.88 >0.85 still fails; M_total Pareto WebMCP 897 vs Stagehand 1773 vs RAG 3703 tokens still shows total saving but not per_hit.

### Calibration — passes

- Stagehand success_n0 1.0 Wilson lower 0.904 ≥0.72, mean success 0.990 ≥0.80, false_accept 0.010 ≤0.10, UNKNOWN_precision 1.0 ≥0.85, ECE_exec 0.005 ≤0.15 bootstrap upper 0.08 ≤0.18, confidence_std 0.057 >0.05, 4 empty bins disclosed, verification-derived (not hash-assigned), probe-derived UNKNOWN — passes C1.
- WebMCP ECE 0.019 similarly passes.

### Pareto

- **M_total_f10 mean per task:** Stagehand 1773 tok /15.2 calls /3682 ms, WebMCP 897/14.3/1799, SPIDER 1087/14.9/1869, RAG 3703/19.3/7265, Cold 5497/22.7/11015, StageCache 4576/20.7/9214. Stagehand dominates RAG/Cold on tokens+latency at n0 (570 vs 747) with accuracy 0.989 ≥0.80, so Pareto C6 reported but not sufficient to overcome per_hit gate. WebMCP Pareto dominates even more (897 vs 1773), confirming total-cost thesis (1104 vs 3663 in parent) but audit V1 metric-design: per_hit hides O(1) saving by construction (both hit same 50 tok verify path where O(1) vs O(N) saving is in retrieval/tool_lookup excluded from per_hit numerator).

### Null controls

- **NC1 shuffled:** rho_per_hit 0.396 p 0.001 >0.25 fails expected |rho|<0.25, but rho_shuffled (block-permutation null) 0.055 <0.20 p 0.42 passes leak gate 0.055<0.35, within-family std 32.8 >0, success 0.58 collapse, crossFamily 0. Per spec precedence PC > |rho_shuffled|>=0.35 gate, NC1 failure alone does not force MEASUREMENT_INVALID (requires shuffled leak which is not triggered). Noted as length-novelty confounding residual.
- **NC2 random:** false_accept 0.151 passes (≥0.10), rho 0.089 <0.25.
- **NC3 length-constant:** rho 0 R2 0 passes.
- **NC4 ablations:** curated +0.65, cache delta 0.086 (8.6% worsening test-warmed), compile delta 7.84 (7x), frontier off worsening 0.12, no-auditor false_accept 0.36 — all show causal deltas >10% where applicable, probe off would worsen >42% (probe saving 0.328).

## Interpretation

With **valid non-degenerate controls PASS** and honest frozen-formula summed counters, **Stagehand selector-cache + TTL freshness gating does NOT achieve pay-cost-of-novelty saving vs retrievable RAG at honest f=10 on this orthogonal 192/36 file-proxy census**: per_hit ratio at n0 1.045>0.85 CI [1.034,1.056] strictly fails, despite probe accuracy 1.0 saving 32.8% and frontier rescue at n≥0.25. Probe fixed overhead (10+50) is dwarfed by 500 tok miss path when DOM-hash cache misses (or frontier rescue still adds 50 tok), so verify 50 dominates retrieval 200 difference. At n0 both Stagehand and RAG hit (50 tok) so probe vs retrieval saving (10 vs 200) is only ~10 tok difference on top of 50 tok verify, yielding near-parity 1.045 not ≤0.85. At n0.25 Stagehand would be miss (500) but frontier Jaccard rescue makes it hit (57) beating RAG (208) where RAG's proportional retrieval is still 200+ hit, so n0.25 appears passing due to frontier, not probe. Overall primary gate F1-TTL fails.

Secondary WebMCP reproduces prior falsification at f=10 (1.032>0.85) and remains >0.85 at f=100 (0.88), confirming **WebMCP 714/2147 O(1) compilation also bounded REJECTED for per_hit on this census**; total-cost Pareto (897 vs 3703) is not gated by per_hit.

Calibration, probe governance, and orthogonal families are intact, so this is a **valid scientific negative** (status COMPLETE, outcome FALSIFIES) not a measurement invalidity. The file-proxy seeded-42 stale decoupled from novelty is a disclosed threat (real CDN fresh at n0 ~1.0 vs 0.53 random).

## Consequences

**Negative:** Per frozen decision_rule, `MIXED` if only calibration or only economics fails, `FALSIFIED` if economics with controls PASS. Here C1 calibration passes but C3 economics fails with C2 PASS => **FALSIFIED_PRIMARY**. Therefore:

- `C-PRODUCT-ECON` remains `HYPOTHESIS` (not `EXPERIMENTAL`) for Stagehand selector-cache+TTL at honest f=10 on this census; do NOT claim pay-cost-of-novelty or freshness-gating viability via selector-cache+gating on file-proxy f=10.
- `C-RESIDUAL-NOVELTY` remains `HYPOTHESIS` (rho 0.472 <0.60, not tracking).
- `C-FRESHNESS` remains `HYPOTHESIS` (probe saving 32.8% demonstrated but not translating to per_hit economics).
- WebMCP secondary: bounded `REJECTED` for this census at f=10 and f=100 per_hit; keep Pareto total-cost observation for future richer DOM.

**Joint falsification triggers PARK** residual-novelty/WebMCP file-proxy economics per Director PIVOT comparative reasoning (this was discriminating pivot before PARK) and pivots Product to runtime honest-cost hardening + HS256 distributed-store repair + richer DOM/QCR post-retrieval before any PRODUCT_CORE claim. No promotion.

## Validity Notes & Threats

- File-proxy synthetic via kernel distill 36/49 ratios with disjoint alphabets; disclosed ceiling not Docker 2000-node full-DOM nor real gpt-4o-mini tokens/browser/latency (rho_proxy_real unmeasured).
- TTL/ETag seeded 42 independence underestimates real CDN fresh at n0 ~1.0; probe-novelty correlation not measured.
- L 8-14 pooled |rho_length| 0.30 >0.20 per-stratum up to 0.476 indicates length confounding despite per_hit isolation; ANOVA not computed.
- ECE over EXEC rows only 150 rows 4 empty bins via softmax temp0.15 jitter disclosed.
- Stagehand DOM-hash simulated via file-proxy, not Playwright CDP AX; frontier rescue inflates Stagehand at n≥0.25 vs pure DOM-hash would be 504 — disclosed optimistic bound but still fails at n0.

## Unresolved

- Docker BrowserGym 0.14.3 2000-node 1280x720 real gpt-4o-mini replication rho_proxy_real≥0.5 would require HS256 shared WAL + BrowserGym availability.
- Whether per-family length normalization would reduce NC1 rho 0.396 to <0.25.
- Whether all-MiniLM QCR changes retrieval-use gap.
- Real CDN staleness correlation impact on probe saving.

## Artifacts

- `fixtures/tasks.json` (391e8f6c) 192/36
- `artifacts/qcr_bank_manifest.json` (8c69804b) frozen bank TAU0.30
- `artifacts/registry.jsonl` (9ac48d20) 36
- `artifacts/webmcp_registry.jsonl` (af3c18e5) 714/2147
- `artifacts/raw_per_task.csv` (a0781aaf) 2112 rows (192*11 systems)
- `artifacts/branch_traces.json` etc with probe/frontier/cacheHit flags
- `src/spider/kernel.py` patched d926279d dot-regex

**Provenance:** run_experiment.py 7a0b8b46, kernel d926279d, base 1044fab7, seed 42, f=10, docker_available false.

