# EXP-PRODUCT-35900911212 — Preregistration

**Lane:** product — `src/spider/kernel.py` + `tests/` + `sdk/` (Research 2.0 Product lane)
**Claims:** `C-RESIDUAL-NOVELTY` (primary, binding `director_mandate PIVOT`) + `C-PRODUCT-ECON` (paired commercial viability)
**Experiment ID:** EXP-PRODUCT-35900911212
**Request:** `research/experiments/EXP-PRODUCT-35900911212/request.json` (hash `fd4f0021...`, base `6f579bd8`)
**Parent handoff:** `research/experiments/EXP-PRODUCT-35892841113/handoff.json` (SUPERSEDE disposition — continuity evidence only per `AGENTS.md`)

> **Transmission invariant:** This prereg + `spec.json` + `request.json` are frozen by deterministic `freeze.json` before any outcome measurement (`research/EXPERIMENT_PACKET.md`). EXECUTE may not mutate frozen inputs; AUDIT recomputes under same metric/control IDs.

---

## 1. Background & why this is the smallest high-information test

**Portfolio state (290 canonical experiments):** Narrow localhost survival (`C-MEAS-VALID` EXPERIMENTAL on Flask/gunicorn+nginx header/body 960/960) but CDN HIT untested; `C-PARAM-INHERIT` synthetic POC survives (10/10, 21/21) but 10 recent WebArena-Verified v2 family holdouts `MEASUREMENT_INVALID` despite durably fixed kernel (dot-aware `_PARAMETER` regex `\$\{[A-Za-z_][A-Za-z0-9_\.]*\}` enabling `${body.sku}`); `C-SEMANTIC-RESOLVE` 40/40 synthetic vs 21/40=0.525 live BrowserGym; `C-RESIDUAL-NOVELTY`/`C-PRODUCT-ECON` **FALSIFIED under honest summed counters** (per_hit SPIDER/RAG 1.0 at n=0, 1.57 at n=0.25, SPIDER/Stagehand 1.61 at n=0) — pay-cost-of-novelty not demonstrated.

**Immediate predecessor EXP-PRODUCT-35892841113 (MEASUREMENT_INVALID, not globally FALSIFIED):** Closed the binding lever — `distill` confidence promoted to 0.85≥0.80 via verified curation + `_template_slots` placeholders consistent with `kernel.py _bind`; audit spot-check 36/36 n=0 tasks `EXECUTABLE` via `kernel.resolve(intent,{family,authenticated},params)` with correct bound body values; per_hit at n0 moved from 512.13 (novel path) to 62.08 (hit path) but still **fails** vs RAG at n0 `1.1339/1.2206>0.85` (producer/frozen formula) while **passes** at n0.25 `0.259/0.282<0.85`; `rho_novelty_per_hit -0.507` (warm-cache `-0.037`) never near `+0.60` with pooled `|rho_length|0.323>0.20`. However packet is `MEASUREMENT_INVALID` per frozen enumeration:

- VF-1 frontier `192/192=1.0` tautology (char-bigram A/B pools share bigrams ~0.63 → every novel slot reconstructable at 50 tok) dominates TERX `0.105` ratios the prereg forbids claiming;
- VF-2 per_hit formula excluded frontier, flipping Stagehand `1.133 PASS` → `1.221 FAIL`;
- VF-3 cache warmed on **test** census (all 36 n0 misses carry 90 extra tok, `cacheHitRate 0.8125 26.875 tok` confounded with level);
- VF-4 `NC` controls are simulated constant `per_hit 500` models (`|rho|=0` guaranteed) not pipeline perturbations;
- plus mislabeled `C1-C6`, decision `C4` rho gate never evaluated.

**Therefore no valid pay-novelty-not-length economics can be claimed** on that census; bounded n0 failure and rho flatness are descriptive only.

**Director mandate PIVOT (binding):** With `C-RESIDUAL-NOVELTY` as binding target, the Global Director (Scout brief + Codex + cognitive reset) selects as highest-leverage question: *does fixing kernel.resolve binding so n=0 hits the 50-tok hit path, plus curated exploration + MEA auditor harness (fresh-context external verified_state before registry update blocking 100% unverified writes) + TTL 60s max-age probe with ~50% stale ETag mismatch exercising, and honest QCR frozen-bank TFIDF Jaccard 0.30 vary-only-post-retrieval, achieve honest `per_hit ≤0.85` vs RAG-EMBED at n0 and n0.25, `≤1.20` vs Stagehand HIT cache at n0, `<1.0` vs TERX at n≥0.25 with `rho≥0.60 |rho_length|<0.20 |rho_shuffled|<0.20` (5000 family-stratified bootstrap + 5000 trajectory-grouped block-permutation) with verification-derived calibration `false_accept≤0.10 UNKNOWN_precision≥0.85 ECE≤0.15`, reporting Pareto vs `gpt-4o-mini+Playwright Docker 2000-node BrowserGym`?*

Comparative reasoning: WebMCP Registry `714 sites 2147 tools O(1)` is high-upside but speculative (requires live sites exposing tools, unmeasured); repeating `FALSIFIED` param-inherit at `n*3200` or `f*6.0` jitter would be measurement-invalid; PARKing without testing the harness that rescues amortized audit/repair overhead (50 tok hit vs 500 tok novel + repair 500 + retrieval 200 + auditor 100) would abandon central commercial claim without testing harness fix.

**Inherited `carry_forward` distinctions (preserved, SUPERSEDE-disposition):**

- *Established (bounded file-proxy ceiling only):* dot-aware binding fix durable (`_PARAMETER` `cfec9866→761aa79d`); bounded n0 `1.13/1.22>0.85` fail / n0.25 pass; rho flatness `−0.507→−0.037` warm-cache; TTL/ETag probe `1.0 accuracy 0.402 saving 0.0 falseAccept` on deterministic map seeded 42; batched cache `0.8125 26.875 tok` blockRate `1.0`; calibration non-vacuous `confidence_std 0.365 UNKNOWN_precision 1.0 false_accept 0.0 ECE 0.0176`.
- *Rejected (bounded to 192/36 file census, not global):* batched MEA at `f=10` `1.13/1.22>0.85` at n0; `rho≥0.60` with `|rho_length|<0.20`; Stagehand `1.133 PASS` (frozen `1.221>1.20`); TERX `<1.0` `0.105` artifact.
- *Unknown (what this experiment repairs/tests):* orthogonal alias families `Jaccard<0.30` hitRate `0.3-0.6` at n=1.0; `f=100` amortization; train-warmed vs test-warmed cache `~0.996` estimate; TTL fresh at n0 real CDN `~1.0` vs `0.53` random; `UNKNOWN`-as-success coding ambiguity; WebMCP `rho_proxy_real`; ECE over EXEC-only `159 rows 4/5 empty`; `frozen-formula` bootstrap CIs.
- *Do_not_assume:* `MEASUREMENT_INVALID` ≠ global `FALSIFIED`; TERX/Stagehand `54.748` floors are tautological reachable-memory; `−0.507` is cache-ordering artifact collapsing to `−0.037`; `NC` constants do not validate pipeline; probe saving does not validate CDN invalidation; `192/36` synthetic ≠ `2000-node 1280x720 BrowserGym` nor real `gpt-4o-mini` economics; frontier `1.0` hitRate is construction artifact — all gated as validity threats below.

**This DESIGN converts the Director's strategic question into the smallest rigorous fix that can change a claim/product decision:** keep the identical 192/36 census, cost model (`f=10` honest summed counters), QCR `TAU0.30`, probe, and harness, but **repair exactly the four measurement-invalid confounds** (orthogonal families, train-warmed cache, frozen-formula honesty, actual-pipeline null controls). No new sites, no new claim, no prior data inspection — do not run outcome-bearing measurements during DESIGN (`AGENTS.md`).

---

## 2. Question, hypothesis, falsifier

**Question (frozen, verbatim from `spec.json`):** With pay-cost-of-novelty FALSIFIED for pure parameterized inheritance at freshness 0.25 under honest kernel-gated cost, does the repaired batched governance pipeline — kernel.resolve dot-aware binding so n=0 hits the 50-tok hit path, curated exploration, MEA auditor batched caching warmed on TRAIN/Curated-A, TTL 60s max-age probe with ~50% stale ETag mismatch exercising, frontier correct-family gating, and honest frozen-bank QCR TFIDF Jaccard TAU0.30 vary-only-post-retrieval over orthogonal alias families (Jaccard <0.30 across families, hitRate 0.3-0.6 at n=1.0 not 1.0) — achieve per_hit ≤0.85 vs RAG-EMBED at n0 and n0.25, ≤1.20 vs Stagehand HIT cache at n0, <1.0 vs TERX at every n≥0.25 with rho_novelty_per_hit≥0.60 |rho_length_per_hit|<0.20 |rho_shuffled|<0.20 (5000 family-stratified bootstrap + 5000 trajectory-grouped block-permutation) on 192/36 WebArena-Verified v2 census (controlled novelty 0/25/50/75/100 train A test never-observed B, L=8-14) with verification-derived calibration false_accept≤0.10 UNKNOWN_precision≥0.85 ECE≤0.15, reporting honest Pareto?

**Hypothesis (falsifiable, per `spec.json`):** The binding defect + measurement confounds are jointly sufficient. Field-path relevant `distill_parameterized` (`body.*|headers.*|url`, `Jaccard≥0.55-0.75` constant-anchor, single-prefix slot induction) will produce `action_template` placeholders matching `kernel.py _bind` dot-regex and `confidence≥0.80`, so `required_slots = parameter_slots ∪ _template_slots(action_template)` are satisfied at `kernel.resolve` and `binding_correctness_n0=1.0 executable_rate_n0=1.0` on 36 n=0 exact-repeat tasks (5/5 per-family spot-check), moving n0 to 50-tok hit path; with orthogonal families (`A/B` disjoint token alphabets, cross-family `Jaccard<0.30` verified, `hitRate 0.3-0.6` at n=1.0) the frontier adapter (`Jaccard≥0.30` in-family only, `crossFamilyAdoption=0`) is no longer tautological; with train-warmed batched cache (`TRAIN/Curated-A` only, first per family `100 tok+80ms` miss then `10 tok+15ms` hits `~28 tok` avg, `blockRate 1.0` both paths) and honest frozen-formula `per_hit=(M_total_f10 − retrieval − distill_amort − auditor_amort)/L` (no frontier exclusion) the SUT will meet all economic, correlation, and calibration gates.

**Falsifier (precedence-ordered, see `spec.json:decision_rule`):**

- Any positive control failure (`PC1` exact-repeat `hitRate 1.0`, `PC2` binding `1.0/1.0 confidence≥0.80 orthogonal <0.30 blockRate 1.0 train-warmed`, `PC3` probe `accuracy≥0.90 saving≥30% falseAccept<0.05`, `PC4` non-vacuous `false_accept 0.10-0.60`) → `MEASUREMENT_INVALID` irrespective of economics.
- Else any `|rho_shuffled|≥0.35 p<0.01` leak, degenerate `CI [1,1]`, `frontierHitRate==1.0` dominating TERX, test-warmed cache artifact, or `within-family std==0` → `MEASUREMENT_INVALID`.
- Else `F1` `SPIDER/RAG>0.85` at n0 or n0.25, `F2` `SPIDER/Stagehand>1.20` at n0, `F3` `SPIDER/TERX≥1.0` at any n≥0.25 (gated if `frontierHitRate==1.0`), `F4` `rho<0.60` or `|rho_length|≥0.20` or `R2_delta≤0.10`, `F5` calibration fail, `F6` governance fail → `FALSIFIED` (or `MIXED` if only `C3` or only `C4` fails) with controls `PASS`.

---

## 3. Baselines, controls, metrics (stable identities for EXECUTE/AUDIT)

**Baselines (identical 192-task orthogonal splits, honest 50-tok hits, frozen-bank same-ranker `TAU0.30`):**

- `B-COLD` — no memory, `500 tok+2 calls` per step + `50+120ms` verify, flat vs `n`.
- `B-RAG-EMBED` — TFIDF Jaccard `TAU0.30` top-1 verbatim `200+150ms`, proportionally retrievable at `n=0.25` (orthogonal families), no MEA/TTL/frontier.
- `B-STAGEHAND-CACHE` — DOM-hash `2000-node 1280x720` serverCache `50+120ms 1 call`, `hitRate 1.0` at n0 else `COLD`.
- `B-TERX-REPLAY` — `0-token` string-equality replay `50 tok` at n0 else `COLD`; **gated** — if `frontierHitRate==1.0` at n≥0.25, `TERX` ratios are `MEASUREMENT_INVALID` per artifact clause (cannot be claimed `PASS`).
- `P-SPIDER-MEA-BATCHED` — SUT as above (curated `confidence≥0.80` + `_template_slots` dot-aware, MEA batched `~28 tok` train-warmed, TTL probe `10+30ms` vs `50+120ms`, frontier `50 tok` correct-family only `TAU0.30`, `freshness 0.25`, `softmax temp0.15+jitter`, honest summed `f=10`).

**Positive control `PC-MEA-BATCHED-TTL-CACHE-ORTHOGONAL`:**

- `PC1` `B-TERX/B-STAGEHAND hitRate 1.0 per_hit ~50 success 1.0` at n0.
- `PC2` `binding_correctness_n0 1.0 executable_rate_n0 1.0 confidence≥0.80 _template_slots present` via actual `kernel.resolve` spot-check `5/5` per family + orthogonal `cross-family Jaccard<0.30` via `qcr_bank_manifest.json` + `hitRate at n1.0 0.3-0.6` + auditor `blockRate 1.0` miss and hit with `cacheHit 0.70-0.85` train-warmed provenance chain.
- `PC3` probe `accuracy≥0.90 saving≥30% falseAccept<0.05` on `~50% stale` deterministic map seeded 42, both paths logged.
- `PC4` non-vacuous `false_accept 0.10-0.60` on forced shuffled adapter via actual pipeline (cache must not bypass).

**Null control `NC-MEA-BATCHED-SHUFFLE-PIPELINE` (all via actual pipeline, trajectory-grouped permutation):**

- `NC1` shuffled `parameter_slots` + auditor hash + frontier keys + `cacheHit` randomization → `|rho|<0.25 |rho_shuffled|<0.20 p≥0.20` (Director `|rho_shuffled|<0.20` sanity), `success≤COLD`, `false_accept 0.10-0.60`, `UNKNOWN≥0.80`, `crossFamily 0`, `within-family std>0`.
- `NC2` random registry/probe/adapter/cache → `false_accept≥0.10` or `|rho|<0.25`.
- `NC3` length-constant `L*500` → `|rho|<0.25 R2<0.15`.
- `NC4` ablations `no-auditor false_accept>0.20`, `uncurated success drop>0.10`, `frontier off` or `cache train-warmed vs test-warmed` `per_hit` worsening `>10%` at n0.

**Primary metrics (honest frozen-formula, `f=10`):**

- `per_hit_ratio_RAG_n0`, `per_hit_ratio_RAG_n0_25`, `per_hit_ratio_Stagehand_n0`, `per_hit_ratio_TERX_n0_25..n1_00` (family-stratified `bootstrap 5000` `95% CI`, `block-permutation 5000` `p`).
- `rho_novelty_per_hit` (pooled Spearman), `rho_length_per_hit`, `rho_shuffled`, `R2_delta_per_hit` (pooled), `R2_novelty/R2_length`, `ANOVA novelty*length`.
- `success_n0`, `mean_success`, `false_accept`, `UNKNOWN_precision`, `ECE_exec` (5-bin, `EXEC` rows only, `confidence_std>0.05`, `3 empty bins` disclosed, `bootstrap 2000` `CI`), `probe_accuracy`, `probe_saving`, `probeFalseAccept`, `auditorBlockRate_miss/hit`, `cacheHitRate`, `effectiveFetchAvg`, `frontierHitRate`, `crossFamilyAdoption`, `curatedDelta`, `qcr_hitRate`, `within_family_std`.

All via summed branch traces `retrieval 200+150ms auditor_fetch_batched cacheHit?10+15:100+80 probe 10+30 vs fullVerify 50+120 hit 50+1 call novel/failed 500+2 repair 500+2 distill 1000/f auditor 100/f frontier 50` — no `n*3200`, no `250+500*int(10n)`, no frontier exclusion.

---

## 4. Design details (what EXECUTE must do, what it must not do)

**Census fidelity (repaired):** WebArena-Verified v2 `192 tasks /36 families ≥3 /49 templates /duplication 0.9479 /param_task 0.8958 /L 8-14` family-specific slots `${sku},${store_id},${variant},{category}` via `src/spider/kernel.py distill_parameterized Jaccard≥0.55-0.75 constant-anchor field-path `body.*|headers.*|url` single-prefix induction. **Repair:** `A/B` pools built from **disjoint token alphabets per family** (orthogonal alias families) so `cross-family Jaccard<0.30` verified and `hitRate at n=1.0` is `0.3-0.6` not `1.0`. Load `/tmp/webarena` or repo-cached `JSON` else generate synthetic orthogonal mock exactly replicating `36/49` ratios with disjoint alphabets; log `fixtures/tasks.json` sha, `registry.jsonl` sha, `qcr_bank_manifest.json` (frozen bank `Curated-A`, `TFIDF Jaccard TAU0.30`, `A/B` disjoint hash), `cost_config.json` (honest `50-tok` hits), `curated_manifest.json`.

**Binding fix (established durable):** `kernel.py _PARAMETER` dot-regex `r"\$\{[A-Za-z_][A-Za-z0-9_\.]*\}"` (`cfec9866→761aa79d`) remains frozen. `induce_registry_curated` writes `Mechanism` with `confidence≥0.80` after verified curation and `action_template` placeholders via `_template_slots` (`body.sku→${body.sku}`) matching `_bind`; preconditions generalized to `family+intent` only. Verify `5/5` per-family `n0` spot-check `EXECUTABLE` with `bound_action` correct via `kernel.resolve`. Log `registry.jsonl` and confidence distribution.

**MEA batched cache — TRAIN-WARMED ONLY (repair):** Fresh-context `25k` truncation, `retrieval` injected at `25k` boundary with provenance graph, `MockEnv verified_state` hash before `distill/update`. Per-family `TTL 60s`: first per family miss `100+80ms` populates on `TRAIN/Curated-A` only, subsequent hits `10+15ms` (`~28 tok` avg), `provenance hash chain` with `cacheHit` flag and `auditorBlocked`. Governance promotes only after `verify` passes even on hit. Audit: `cacheHitRate 0.70-0.85` with per-step `probeHit/etagMatched/ttlValid/cacheHit/frontierHit` flags; verify `TRAIN`-only warming (hypothetical test-warming would give `36/36` misses `90/L` inflation at n0).

**TTL/ETag probe:** Conditional `HEAD If-None-Match ETag W/body_sha TTL 60s max_age` via deterministic `TTL/ETag` map `seeded 42` (`ttl_created [0,120]` vs `current [0,200]` `~50% fresh ~50% stale` exercising mismatch). `10+30ms` vs `50+120ms`. Honest summed counters; `accuracy≥0.90 saving≥30% falseAccept<0.05` required. Threat disclosed: deterministic map independence from novelty decouples `freshness` from `novelty` (real CDN `fresh at n0 ~1.0` vs `0.53` random).

**Controlled novelty:** Per-family disjoint `Curated-A(train)/B(test never-observed)` orthogonal pools `zero overlap` frozen bank `TAU0.30` same ranker for all retrievers. Fractions `n {0,0.25,0.50,0.75,1.00}` `n` fraction slots from `B` `(1-n)` from `A` stratified by `header vs url` and family; `n=0` exact-repeat for `TERX/Stagehand` `1.0` reachable but orthogonal ensures `hitRate at n≥0.25` is `0.3-0.6`. `Train 5 demos/family` on `A` only `1 Mechanism/family`. Frontier adapter `family_id` key `Jaccard≥0.30` in-family only `crossFamily 0` `50 tok`. All fit on `TRAIN` only. Log realized novelty per task for `S=1/2/3` families.

**Length & per_hit isolation (repaired):** `L 8-14` constant within family, orthogonal to `n` within strata. Primary is `M_per_hit=(M_total_f10 − retrieval − distill_amort − auditor_amort)/L` (`f=10`) — **no frontier exclusion** (frontier cost stays in both `M_total` and `per_hit`); secondary `M_total_f10`. Report `probe split`, `frontier split`, `cacheHit split`, `Spearman rho_novelty_per_hit`/`rho_length` pooled with `family-stratified bootstrap 5000` + `trajectory-grouped block-permutation 5000` per Director prior `|rho_shuffled|<0.20`. `within-family std>0` required; degenerate `[1,1]` `CI` flagged `degenerate not precision`.

**Statistics:** Primary `rho M_per_hit vs n` (secondary `rho_total`) + `rho_length` pooled `family-stratified block-permutation` (`family-label` permutation `5000`) + `bootstrap 5000` for `95% CI` on `rho,R2_delta,ratio,probe_saving,auditor_precision,frontierHitRate,cacheHitRate,curatedDelta`. `Degenerate [1,1]` flagged. `QCR` bank hash, `Docker` availability flag in `provenance.json`. Exploratory `f=100` amortization (`distill 10 tok vs 100 auditor 1 vs 10`) as secondary analysis (does not gate `SURVIVES`).

**Docker exploratory (does not gate `SURVIVES`):** If `runtime` distributed `HS256 JWT` + `BrowserGym 0.14.3 CDP AX 2000-node 1280x720 + gpt-4o-mini 15-step + Playwright 1.63` available, replicate subset with real `tokens/browser_calls/latency` and report `Pareto` alongside proxy with `rho_proxy_real` correlation; if unavailable disclose `proxy-only` bounded to file mock and log `failure.json` smallest next action. This discloses the `148 tok` fixed overhead decomposition (`28 tok auditor avg +50 frontier +50 distill/auditor amort` plus probe saving `~40`).

---

## 5. Decision rule (frozen — summary, full in `spec.json`)

**Primary census:** family-stratified pooled `N~192` proxy `f=10` train-warmed orthogonal; Docker exploratory does not gate but informs `Pareto` and `rho_proxy_real`. Compute per-method `success,false_accept,UNKNOWN_precision,ECE_exec,M_total_f10,M_per_hit`, `rho_novelty_per_hit` (primary), `rho_total`, `rho_length` pooled, `R2`, `R2_delta`, `per_hit parity ratios` (frozen formula), `Wilson95%`, `bootstrap5000` `CI`, `block-permutation5000` `p` and `|rho_shuffled|<0.20 p≥0.20 + within-f std>0`.

- **`SURVIVES_CURRENT_TEST` iff ALL:**
  - `C1` correctness+calibration `success_n0≥0.85 Wilson lower≥0.72 mean≥0.80 false_accept≤0.10 UNKNOWN_precision≥0.85 ECE_exec≤0.15 confidence_std>0.05`;
  - `C2` positive controls `PC1` `hitRate 1.0 ~50 tok` + `PC2` `1.0/1.0 confidence≥0.80 slots orthogonal <0.30 hitRate 0.3-0.6 blockRate 1.0` train-warmed `0.70-0.85` + `PC3` `accuracy≥0.90 saving≥30% falseAccept<0.05` + `PC4` non-vacuous `0.10-0.60`;
  - `C3` economics via frozen formula `≤0.85` vs `RAG` at n0 **and** n0.25, `≤1.20` vs `Stagehand` at n0, `<1.0` vs `TERX` at every n≥0.25 (four levels) unless `frontierHitRate==1.0` gates `TERX`;
  - `C4` `rho≥0.60 block p<0.01 bootstrap lower≥0.40` and `|rho_length|<0.20 upper<0.30` + `R2_delta>0.10` + `NC1 |rho_shuffled|<0.20 p≥0.20 within-f std>0`;
  - `C5` governance `probe` + `blockRate 1.0` + `crossFamily 0` + `orthogonal <0.30` + `curatedDelta>0.10`;
  - `C6` `Pareto` reported.

- `MIXED` if `C3` fails but `C4` passes or vice versa with `C2` passing.
- `FALSIFIED` if `C3` or `C4` fail with `C2` non-degenerate.
- `MEASUREMENT_INVALID` if any `PC` fails or degenerate `CI` or `frontier==1.0` dominating `TERX` or `NC1` leak or cache test-warmed or `within-f std==0`. **Precedence:** `PC failure > NC1 leak > frontier artifact > FALSIFIED`.

**Exploratory `f=100`:** report `per_hit` with `distill 10 tok auditor 1 tok` to test whether `1.22→<0.85` flips, but does not override `f=10` gate.

---

## 6. Product consequences

**If `SURVIVES` with `PC1-PC4 PASS` (orthogonal verified, train-warmed, frozen-formula honest, actual-pipeline `NC`):** `C-RESIDUAL-NOVELTY` `HYPOTHESIS→EXPERIMENTAL` bounded to `WebArena-Verified v2` orthogonal file-based census `192/36` proxy with binding-fixed curated exploration + MEA batched `~28 tok` `TRAIN`-warmed + TTL probe + frontier correct-family `TAU0.30` under `QCR` honest `f=10`. First evidence that governed-memory + cheap verification + correct-family reconstruction + train-warmed caching achieves honest `per_hit` targets that prior pivots falsified at `1.0-1.61` and parent `1.13/1.22` artifact. Unblocks `C-PRODUCT-ECON` via validation+reconstruction and `C-FRESHNESS` via `TTL/ETag`. Justifies promoting MEA batched harness+probe+adapter as product lever vs selector cache despite `Stagehand 80%` at exact repeat. **No `PRODUCT_CORE` promotion** without `Docker 2000-node 1280x720 + real gpt-4o-mini` replication and `rho_proxy_real≥0.50`.

**If `FALSIFIED` (controls `PASS` non-degenerate orthogonal):** Repaired batched governance (curated+`TRAIN`-warmed `~28 tok`+`TTL`+`orthogonal` frontier) does **not** yield residual-novelty-proportional compression vs retrievable `RAG` or shipped `Stagehand` at honest `f=10`; either `148 tok` fixed overhead (`28+50+50+20` amort) still dominates at n0 despite `50-tok` hit path, or orthogonal frontier not beating `RAG`, or rho flatness persists. Product **must NOT claim** pay-cost-of-novelty for `C-RESIDUAL-NOVELTY/C-PRODUCT-ECON` via this harness on this setting; acknowledge `Stagehand 80%` at exact repeat and `RAG` at `n0.25` remain strong baselines. Per Director comparative reasoning this is the **last discriminating batched-MEA test before PARKing residual-novelty and pivoting Product to WebMCP tool-bypass compilation (`714 sites 2147 tools O(1)`)** as primary lever; bounded `REJECTED` for this orthogonal proxy `f=10` only, not global falsification (may transfer with richer DOM, `f=100`, `HS256` substrate). No promotion; `Pareto` decomposes overhead.

**If `MIXED`:** keep `HYPOTHESIS` and investigate overhead dominance vs `per_hit` isolation.

**If `MEASUREMENT_INVALID`:** binding/orthogonal/cache fix insufficient → require kernel `preconditions/template` or disjoint alphabet re-fix before any economics claim.

---

## 7. Validity threats & disclosure (preregistered)

- Deterministic `TTL/ETag` map `seeded 42` independence from novelty underestimates real CDN `fresh at n0 ~1.0` vs `0.53` random and probe-novelty correlation; no cache-invalidation correlation measured — threat disclosed, not removed (exploratory `gunicorn+nginx` loopback `ETag W/body_sha max-age 60` if `BrowserGym` available).
- Nominal `n=0.25` realizes as `0.0/0.333/0.5` for `S=1/2/3` slot families (coarse `1/2/3` slot grid, `9` exact-repeats in `n0.25` bucket) — disclosed, pooled `rho` primary.
- `L` `8-14` varies across families (orthogonal within strata) — isolated via `per_hit` frozen formula; `ANOVA novelty*length` and within-stratum `rho_length` disclosed.
- `ECE_exec` over `EXEC` rows only (`159` rows `4/5` bins empty `confidence_std 0.365` via `softmax temp0.15+jitter` seeded) — `EXEC`-only disclosed, not vacuously `UNKNOWN`-inflated.
- `frontier` correct-family `Jaccard≥0.30` still tautological if cross-family `Jaccard` not `<0.30` — gated by orthogonal check; `TERX` `0.105` artifact prohibited per artifact clause.
- File-based synthetic `192/36` `49` templates `duplication 0.9479` via actual `kernel distill_parameterized` ≠ `Docker BrowserGym 2000-node 1280x720` `cross-site` nor real `gpt-4o-mini` token economics (`docker_available false` `numpy/sklearn` unavailable, `BrowserGym` not required for primary gate) — `rho_proxy_real` unmeasured in proxy-only run, disclosed bounded ceiling.
- Laplace smoothing inflates `H` with cell count, `SHA256` truncation destroys `AX` info, deterministic bootstrap at ceiling `1.0` hides sensitivity, per-node `SQLite` under round-robin breaks session — per Director prior, demand `trajectory-grouped permutation`, `non-hash-truncated AX up to 5k`, `shared WAL+sticky hash` for future `Docker` replication; proxy `MockEnv` branch-derived threat disclosed.
- `UNKNOWN`-as-success coding `success=1` whenever `would_verify` fails vs strict `UNKNOWN` excluded (`n0.5 0.7436<0.80 overall 0.8307`) — ambiguous packet coding disclosed; both reported.

---

## 8. Estimated cost & expected information gain

**Cost:** Low-moderate file-based `~1728` deterministic `resolve/_bind/MEA-batched-verify/TTL_probe/frontierAdapter` trials on orthogonal `A/B` disjoint alphabets plus `~768` ablations plus `TFIDF` offline and `wrong-bound p=0.15` branches plus train-warmed `hit/miss` audit. `Wall <60min` CPU proxy (`<100min` if `Playwright 2000-node` loopback). Storage `~2700` rows `CSV` `registry.jsonl` `qcr_bank_manifest` `branch_traces` with `orthogonal` `probe/auditor/cacheHit/frontier` flags. Exploratory `Docker+gpt-4o-mini` `~3000` browser calls `~2000` LLM calls `<$15`.

**Information gain:** Very high and decisive — repairs all four `MEASUREMENT_INVALID` causes from parent while preserving binding lever, making this the first *valid* falsifier for whether verification-auditor pipeline rescues pay-cost-of-novelty where pure parameterization failed. Either valid positive (`≤0.85` at n0/n0.25 with `rho≥0.60`) reopens `≥25%` honest saving and validates batched governance before PARKing, or valid negative (`>1.0` vs `RAG` despite `50-tok` hit path) bounded `REJECTS` batched inheritance at honest `f=10` and pivots `Product` to `WebMCP` tool-bypass — either outcome definitively decides Product architecture (batched distillation vs selector cache vs `WebMCP` compilation) with `Pareto` and `rho_proxy_real`.

---

## 9. Analysis plan (no outcome-bearing measurement before freeze)

No analysis before `freeze.json`. `EXECUTE` will:

1. Freeze `request.json` `spec.json` `prereg.md` hashes in `freeze.json`.
2. Generate/load `orthogonal` census (`fixtures/tasks.json` `qcr_bank_manifest.json` `artifacts/qcr_bank_manifest.json` `registry.jsonl`) verified `cross-family Jaccard<0.30`.
3. Run all baselines + SUT + `NC1-NC4` via actual `kernel.resolve/_bind/MEA-batched-verify/frontierAdapter/MockEnv` with `seeded 42` deterministic `TTL/ETag` map `~50%` stale and train-warmed cache, logging per-task `branch_traces.csv` with summed counters (no `n*3200`), `raw_per_task.csv`, `probe_traces.json`, `cache_traces.json`, `frontier_adapter_traces.json`, `derived_metrics.json` (bootstrap/permutation `CI`).
4. Compute frozen-formula `per_hit` and all `PC/NC` checks; apply decision rule precedence; write `result.json` (required `schema_version,experiment_id,lane,status,outcome,metrics,controls,artifacts,observations,validity_notes,unresolved`) + `report.md` + `provenance.json` (commits `kernel.py 761aa79d`, `run_experiment.py` sha, `docker_available` flag, `gunicorn+nginx` simulated).
5. `AUDIT` recomputes `per_hit` via frozen formula, `rho` via trajectory-grouped permutation, `NC` via actual pipeline, checks orthogonal `Jaccard`, cache warm source, `frontierHitRate` gate.

No `git commit/push/switch/reset` in `DESIGN`; `DESIGN` fills only `spec.json` + `prereg.md`.

