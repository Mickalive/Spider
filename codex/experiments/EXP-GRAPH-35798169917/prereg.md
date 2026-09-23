# EXP-GRAPH-35798169917 — Preregistration (Research 2.0 Graph, C-PARAM-INHERIT single-family pilot)

**Lane:** graph · **Claim:** C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers) · **Mode:** REOPEN (Director mandate, binding) · **Status:** DESIGN (pre-freeze)

## 1. Scientific question (Director mandate, binding)

> After genuinely fixing `src/spider/kernel.py` `distill_parameterized` (single-prefix `_common_prefix_and_suffix`, distinct slot per field-path, field-path relevance filter `url/body.*/headers.*` only, Jaccard `>=0.75` constant-anchor check, confidence `0.90`) verified by code inspection and unit tests with zero unsubstituted templates, does a narrowed single-family WebArena-Verified v2 pilot (train 3-5 exemplars of one family on resource A, test zero-overlap resource B, `>=10` tasks family, family-stratified bootstrap CIs) achieve `EXECUTABLE >=0.75` and binding correctness `>=0.90` with success margin `>=0.12` vs `B-COLD`/`B-RAG`/`B-REPLAY-TERX`/`B-INSTR`, `false_accept <=0.10` `UNKNOWN` in `[0.00,0.15]` `ECE <=0.15`, with honest `tokens+browser+retrieval+verification` cost at `f=10`?

**Director allocation:** `REOPEN` C-PARAM-INHERIT. `parent_handoff_disposition: SUPERSEDE`. Comparative reasoning: continuing to WebArena-Verified v2 family hold-out on buggy kernel repeats last 3 MEASUREMENT_INVALID (0% info gain); pivoting now to PreAct state-machine is orthogonal but premature before confirming minimal slot-induction fix suffices; delta-repair on nginx is lower leverage than unblocking param inheritance which gates C-RESIDUAL-NOVELTY and C-LLM-INHERIT. Narrowed single-family pilot is smallest discriminating test vs exhaustive 10-family 192-task sweep on broken code. Dependencies: `runtime:C-MEAS-VALID nginx HIT substrate 960/960` for honest verification cost, `intel:C-CROSSSITE 20-sample AX consistency at 1280x720` for family isolation.

**Inherited parent handoff:** `EXP-GRAPH-35793560957` `MEASUREMENT_INVALID` (no LLM, synthetic census 275 tasks duplication 0.8182 vs target 0.9479, tasks_valid 7<10, transient kernel sha 04438d... not persisted to HEAD sha 46929b3a... literal-only 132 lines, grep 0 hits distill_parameterized, tests/test_kernel_param_inherit.py absent). Its `next_question` is advisory continuity only; Director mandate REOPEN is binding and SUPERSEDE. This prereg preserves the four-way distinction exactly:

**Established (must not be re-proven as new):**
- C-PARAM-INHERIT is `EXPERIMENTAL` only at narrow synthetic ceiling: `EXP-PRODUCT-33528829801` audit PASS 10/10 single-param common-prefix deterministic single-field, and `EXP-PRODUCT-33741671686` audit PASS 21/21 harness-only multi-param (`run_experiment.py` only, not `src/spider/kernel.py`, fragile positional mapping), plus committed-code synthetic single-slot Fix1/2/3 on `src/spider/kernel.py` per product chain — not extended by this pilot (audit claim_ceiling).
- WebArena-Verified v2 census target remains loadable in principle per `EXP-INTEL-35749371101` audit PASS 192 tasks/49 templates duplication 0.9479 [0.9167,0.9792] exact_copy 0.0781 param_task 0.8958 families_ge3 36 AX 0.9 on 20 CDP trees via Docker `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945` hash `d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30` — but last packet used synthetic fallback 275 tasks duplication 0.8182 (MEASUREMENT_INVALID for WebArena claim).
- Infrastructure for last packet: transient kernel patch sha 04438d... with 7 functions verified and 16/16 tests PASS but NOT persisted to HEAD (46929b3a... literal-only, git diff empty), artifacts absent at audit, llm_available false, tasks_valid 7<10.

**Rejected / do_not_assume:**
- Bijective cost `250+500*10*novelty` and hardcoded 72-task `0.9479` mock are MEASUREMENT_INVALID (tautological rho=1.0) — rejected per Director mandate; only honest tokens+browser+retrieval+verification counts.
- Reported `kernel_check.json` 7-check PASS in parent is rejected as fabricated transient; src/spider/kernel.py lacks distill_parameterized entirely at HEAD — do not cite as evidence until git diff nonempty, sha matches claimed, grep hits present and audit PASS.
- MEASUREMENT_INVALID (0 tasks, missing LLM/census) is not falsification of parameterized inheritance — C-PARAM-INHERIT remains EXPERIMENTAL not REJECTED.
- PC2 synthetic same-A multi-param success in harness (21/21) does not demonstrate A->B generalization — ceiling remains harness-local induction on A.
- Synthetic census 275 tasks duplication 0.8182 is rejected as WebArena evidence; requires real Docker census hash d652756... with duplication within CI.

**Unknown (this experiment must resolve):**
Does genuinely fixed `distill_parameterized` (single-prefix, field-path relevance filter url/body.*/headers.* only, Jaccard >=0.75 distinct slot per field-path, confidence 0.90) when durably committed to src/spider/kernel.py and exercised via real registry required_slots|template_slots/_bind/verify enable EXECUTABLE>=0.75 binding>=0.90 zero unsubstituted templates on never-observed B with zero overlap, success margin >=0.12 vs each baseline, false_accept<=0.10 UNKNOWN [0,0.15] ECE<=0.15 with honest f=10 cost? Plus controls, verification AUROC, contamination, and cost ratios.

**Agent priors used (distinguished from SPIDER evidence per mandate):**
Prior: Tool-use agents accumulate path-dependent context salience and self-generated subproblems over long horizons; without verification/UNKNOWN abstention they compound planning errors — distinguished from SPIDER evidence which only shows degenerate [:20] truncation and cross-family key adoption inflation but not general horizon effect. Prior: Replay beating cold is weak; strong baselines are RAG, TERX 0-token replay with guards, instruction-augmented agents on same model/budget — SPIDER evidence: EXP-FRONTIER shows no discriminability vs flat RAG when oracle disabled, TERX 0-token replay never beaten on WebArena-Verified v2. Prior: Memory that might be wrong is worse than no memory: staleness false-accept dominates economics, not hit-rate — SPIDER evidence: C-FRESHNESS r=0.041 confirmed on localhost but distributed session non-replication makes FP=0.0 invalid on deployment. Prior: State representation crux: URL+hash truncation tautologies isomorphic to SHA256(L); visual/AX structure survives CSS refactors — SPIDER evidence: EXP-PHYSICS tautology and [:20] truncation are Codex-established failures. Prior: Exploration cost is tool+observation+verification loops; amortized cost at f=10 vs f=100 changes decision, bijective cost=n*novelty hides length confound — SPIDER evidence: EXP-PRODUCT FALSIFIED shows rho_length confounded by n*3200.

## 2. Hypothesis

`H1`: A corrected `distill_parameterized()` with three fixes — (a) single-prefix `_common_prefix_and_suffix` (no double-prefix truncation so `user-4` binds fully), (b) field-path relevance filter restricting `_extract_varying_values` to `url/path`, `body.*`, `headers.*` only (excluding top-level metadata/provenance noise), (c) structure-similarity `Jaccard >=0.75` constant-anchor to reject `E1` hallucination — with distinct slot naming per field-path (`body.sku -> ${sku}`, `headers.X-Csrf-Token -> ${csrf_token}`, `url path segment -> ${resource_id}`) at confidence 0.90 ported to `src/spider/kernel.py` and verified by code inspection + unit tests with zero unsubstituted templates, will allow 3–5 exemplars of **one** family on resource **A** to induce a mechanism that on never-observed resource **B** (zero value overlap) resolves `EXECUTABLE >=0.75`, binds correctly `>=0.90`, leaves zero `${}` templates, beats each baseline by `>=0.12` success, keeps `false_accept <=0.10` `UNKNOWN [0,0.15]` `ECE <=0.15`.

`H0` (null): Transfer does not exceed baselines; literal/retrieval/replay already capture any `0.9479` duplication that is exact-copy `0.0781`-limited; parameterization adds no margin or violates safety/calibration. Cost at f=10 is secondary.

## 3. State, action, target, unit of analysis

- **State representation:** raw `context` dict passed to `resolve()` (preconditions + applicability guards). No hidden site-id leakage; family hold-out ensures test family never seen during distill.
- **Action representation:** `action_template` dict with parameterized slots `${slot}`. Slots named per field-path (`body.sku -> ${sku}` etc.). Binding via `_bind()` on `required_slots | _template_slots`. Zero unsubstituted templates required among EXECUTABLE.
- **Target:** Per-task `success` = deterministic postcondition `_matches(mechanism.postconditions, observed_state)` after Playwright execution (not LLM-as-judge). Plus mechanism quality: `EXECUTABLE` rate, `binding_correctness` (bound_action equals gold B identifier), `unsubstituted_templates` count.
- **Unit of analysis:** task. For single-family pilot, family is the block but `n>=10` tasks within one family; bootstrap is family-stratified task bootstrap (collapses to task bootstrap for single family, disclosed). Future 10-family scale-up will use family as block.

## 4. Sampling policy & holdout

- **Dataset:** WebArena-Verified v2 shopping census: load from `data/webarena_verified_v2.json`, `/tmp/webarena`, or Docker `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945` or verified CSV (3 fetch attempts, hash logged). Dedup by `template+intent` hash as in `EXP-INTEL-35749371101`. Verify duplication `0.9479` and exact_copy `0.0781` within CI [0.9167,0.9792] or log deviation.
- **Pilot selection:** Choose `>=1` family with `>=10` tasks after dedup. Require `>=2` disjoint resource pools `A`/`B` within that family (SKU/store/user IDs). Training uses 3–5 exemplars from **A** only; **B** values have zero exact overlap with **A** for parameterized slots (`value_set_A ∩ B = ∅` verified, logged in `provenance.json` with hashes). Family hold-out (not random split) prevents site identity leakage. Minimum `10` valid tasks required for decision; target `12–20` if budget allows. Claim ceiling bounded to pilot family, not 10-family generalization. Dependencies: intel 20-sample AX consistency ensures family isolation at 1280x720.
- **Exclusions:** tasks with `>50%` LLM API failure, Playwright timeout `>30s`, or census load failure are excluded and counted; if `<10` valid tasks remain → `MEASUREMENT_INVALID`.
- **Model:** `gpt-4o-mini-2024-07-18` (or approved `haiku`/`flash` equivalent), `temp 0.0`, `seed 42`, `max 15` steps, `4096` tokens, identical Playwright toolset `navigate/click/fill/type/select/goBack/observe` on `chromium` headless, `PYTHONHASHSEED=0`.
- **Why single-family:** Smallest high-information test that can change claim/product decision per Director allocation comparative_reasoning: higher leverage than DELTA-REPAIR BLOCKED x4 repeat or FRESHNESS distributed fix, prerequisite for honest residual-novelty economics. Powered `n=10` is existence proof, not definitive margin-precision.

## 5. Kernel fixes (what EXECUTE must verify before measuring)

Fixes must be in `src/spider/kernel.py` (graph allowed to patch `src` per Director REOPEN), not only harness:

1. `_common_prefix_and_suffix` uses **single-prefix** (common prefix only, no double-prefix that truncates `user-4` → `4`).
2. `_extract_varying_values` field-path filter: allow only `url`, `body.*`, `headers.*` (and `path`); reject top-level `provenance`/`state` noise — verified via `_is_allowed_path` grep.
3. `structure_similarity` `Jaccard >=0.75` constant-anchor check to reject `E1` hallucination when values lack common structure (two-part check `Jaccard>=0.75` + constant-value anchor).
4. Distinct slot naming per field-path via `_field_path_to_slot_name`/`_sanitize_slot`, `confidence 0.90`, stored via registry `parameter_slots` + `action_template` with `required_slots | _template_slots` gating and `_bind` resolution. Single-prefix handling must keep full `user-4` not suffix-only `4`; test with `C2` `user-4` vs `user-5`. Zero unsubstituted templates among EXECUTABLE is required.

**Verification gate before outcome measurement:** code inspection (`grep distill_parameterized/_common_prefix_and_suffix/Jaccard/_is_allowed_path/_field_path_to_slot_name`) + `sha256` logged + `git diff` vs `base_sha c065bc92f8b56ab2ddfdaa0612097ee7fbe7a953` + unit tests `tests/test_kernel_param_inherit.py`: `B1`/`B4` clean-synthetic regression still pass, `D1` noisy over-param and `E1` hallucination correctly rejected, `B2/B3/B5` short-value and `C2` `user-4` full-value cases, plus `distinct slot per field-path` test and zero `${}` template verification. If gate fails → `MEASUREMENT_INVALID`, no claim inference. Report actual `src/spider/kernel.py` sha256 and diff in `provenance.json`; do not fabricate without audit recomputation. Runtime nginx HIT 960/960 substrate should be noted but not blocking honest cost.

## 6. Baselines (strong, same B set, same LLM/tools/verification)

| ID | Mechanism | Cost accounting |
|---|---|---|
| `B-COLD` | Cold LLM, no memory | `LLM tok + browser calls+ms + latency` |
| `B-RAG` | RAG `Jaccard 0.30` retrieval, verbatim replay without slots; `200 tok` retrieval + fallback to COLD on mismatch | measured hit/miss via `_matches` |
| `B-REPLAY-TERX` | 0-token exact replay: exact `action_template` equality → `0 tok +1 verify (50 tok, 90ms)` else fallback to COLD | `hit_rate` expected `~0` on hold-out |
| `B-INSTR` | Hand-authored site instructions, no slots; instruction `200 tok` amortized `200/f` | same verification |
| `B-LITERAL` | Literal `distill()` without slots, exact registry match | confirms param necessity; success `>0.15` signals leakage |

All baselines run on the **identical** pilot B set with identical budget and deterministic `_matches` verification. Costs measured via API `usage` tokens + browser `ms`, not formulas. All baselines share same `model/tools/verification/postconditions` so `success` denominator is identical. Honest cost honest `tokens+browser+retrieval+verification` at f=10 primary.

## 7. Controls

- **Positive** `PC-PARAM-REGRESSION-AND-LITERAL-HIT` (stable IDs `PC1`, `PC2`):
  - `PC1` same-A literal hit via `B-REPLAY-TERX`: `hit_rate 1.0`, `cost 50 tok`, `success 1.0`.
  - `PC2` multi-param same-A via `distill_parameterized` on 3–5 A exemplars, same `A` via registry `_bind`/`verify`: `EXECUTABLE 1.0`, `binding 1.0`, `success >=0.90`, zero templates.
  Failure → `MEASUREMENT_INVALID` (substrate broken, not falsification).

- **Null** `NC-SHUFFLED-AND-RANDOM` (stable IDs `NC1`, `NC2`, through real `bind`/`verify`):
  - `NC1` shuffled slot mapping (permute slots): expected `success <= B-COLD+0.05`, `false_accept >=0.25`, `binding <0.50`.
  - `NC2` random retrieval: expected `false_accept >=0.30` or `success <= B-COLD`.
  If `NC1 success >= SPIDER-0.05` → SPIDER effect spurious → `FALSIFIED` not `SURVIVES`.

Stable metric IDs: `M-EXECUTABLE-SPIDER`, `M-BINDING-CORRECT`, `M-UNSUBSTITUTED-TEMPLATES`, `M-SUCCESS-SPIDER`, `M-SUCCESS-COLD`, `M-SUCCESS-RAG`, `M-SUCCESS-REPLAY`, `M-SUCCESS-INSTR`, `M-SUCCESS-LITERAL`, `M-FALSE-ACCEPT-SPIDER`, `M-UNKNOWN-RATE`, `M-ECE`, `M-COST-SPIDER`, `M-COST-COLD`, `M-COST-RAG`, `M-AMORTIZED-SAVING-vs-COLD`, `M-COST-RATIO-RAG`, `M-CONTAMINATION`.

## 8. Metrics, uncertainty, and decision rule (frozen)

**Primary metrics on pilot B (real LLM+Playwright, not proxy):**
- `M-EXECUTABLE-SPIDER` (rate `EXECUTABLE` resolutions), Wilson 95% CI.
- `M-BINDING-CORRECT` (correct `bound_action` among `EXECUTABLE`), Wilson 95% CI.
- `M-UNSUBSTITUTED-TEMPLATES` (count of remaining `${}` in `bound_action` among `EXECUTABLE`; must be 0).
- `M-SUCCESS-*` per baseline, deterministic `_matches`.
- `M-FALSE-ACCEPT` (verification passed but binding wrong), `M-UNKNOWN-RATE` (abstentions), `M-ECE` (10 bins, confidence vs success), `verification AUROC` where measurable, `M-CONTAMINATION <0.10`.

**Uncertainty:** Family-stratified task bootstrap `5000` resamples `seed 42` (family-block collapses to task bootstrap for single family, disclosed); paired McNemar for success margins where `n` permits; family-stratified bootstrap CIs as mandated. Wilson 95% CI for EXECUTABLE and binding correctness. Report both. Disclose power: at `n=10`, power to detect `0.12` delta from `0.45` baseline is ~`0.25` (pilot is existence proof, CIs will be wide).

**Adequacy rule:** `>=10` valid B tasks with zero-overlap proof and kernel gate PASS (zero unsubstituted templates verified) and `census_verified true` with hash logged. Otherwise `MEASUREMENT_INVALID`. Also require `OPENAI_API_KEY` present flag and Playwright available; if `>50%` trials LLM unavailable → `MEASUREMENT_INVALID`.

**Decision rule (frozen):**

`SURVIVES_CURRENT_TEST` requires **all** `C1–C5`:

- `C1` success: `M-SUCCESS-SPIDER >=0.65` and `> B-COLD +0.12` and `> B-RAG +0.12` and `> B-REPLAY +0.12` and `> B-INSTR +0.10`, family-stratified bootstrap `95%` CI lower `>0.02` for each margin, McNemar `p<0.05` where `n` permits.
- `C2` mechanism: `M-EXECUTABLE-SPIDER >=0.75` (Wilson lower `>=0.65`) and `M-BINDING-CORRECT >=0.90` (Wilson lower `>=0.80`) with `M-UNSUBSTITUTED-TEMPLATES =0`.
- `C3` safety: `M-FALSE-ACCEPT-SPIDER <=0.10` and `M-UNKNOWN-RATE in [0.00,0.15]` and `B-LITERAL success <=0.15` on same B.
- `C4` controls: `PC1` `hit_rate 1.0` `50 tok` `success 1.0` PASS and `PC2` `1.0/1.0/>=0.90` PASS; `NC1` `success <= COLD+0.05` and `false_accept >=0.25` and `NC2` `false_accept >=0.30` or `success <= COLD`.
- `C5` calibration: `UNKNOWN` cases have `confidence <0.80` or missing slots, `M-ECE <=0.15` (10 bins), `AUROC >=0.75` where measurable, `M-CONTAMINATION <0.10`.

Secondary `C6` economics `E-ECON` is **reported** not gating for `SURVIVES` in this pilot: `M-AMORTIZED-SAVING-vs-COLD` at `f=10` and `M-COST-RATIO-RAG` with bootstrap CIs. If `saving >=25%` and `ratio <=0.85` with `CI` not crossing `1.0`, product economics strengthened but not required due to limited `n`. Report both raw and amortized `f=1,10,100`.

`FALSIFIED` if any `C1–C3` fails on valid substrate (excluding `PC`/`NC` substrate failures which are `MEASUREMENT_INVALID`). `MIXED` if `C1` margin fails but `C2` passes (binds correctly but agent fails downstream verification/repair within 1 step → investigate Playwright/verification, not just induction). `MEASUREMENT_INVALID` if kernel not durably ported via `src/spider/kernel.py` diff/sha256 with zero templates, `<10` valid tasks, census not verified, `>50%` LLM failures, verification broken, or family hold-out leakage (`value_set_A ∩ B !=0`).

## 9. Cost accounting (honest, amortized)

Per-task: `cost = LLM input+output tok (API usage) + browser calls+ms + retrieval 200 tok + verification 50 tok + repair 1 step if verification fails`. `distill ~1000 tok` amortized `1000/f` **only** to SPIDER; instruction `200/f` only to `B-INSTR`. Report raw and amortized `f=1,10,100` with family-stratified task bootstrap `5000 seed 42` CIs for `M-AMORTIZED-SAVING-vs-COLD` and `M-COST-RATIO-RAG`. Latency = `LLM + browser + retrieval + verification + repair`. Token, browser, latency reported separately and combined. No bijective formula; honest branch-derived cost from actual kernel `resolve`/`_bind`/`verify`/`freshness` gating required. Primary metric is honest `tokens+browser+retrieval+verification` at `f=10` per Director mandate.

## 10. Validity threats and mitigations

- **Ceiling degeneracy:** Pilot family may be trivial (all bodies discriminate `1.0`). Mitigation: choose family with at least `path+body+headers` variation; require `PC2` multi-param (not single-field) and report per-slot binding, zero unsubstituted templates, and runtime nginx HIT verification.
- **Singleton template tautology:** binding correctness via deterministic identifier equality with zero_overlap_verified, not PMI; zero unsubstituted templates gates tautology.
- **Site leakage:** Random split would leak site identity. Mitigation: family hold-out with `value_set` intersection proof `=0` logged; `B-LITERAL` leakage check `<=0.15`; intel 20-sample AX 1280x720 ensures family isolation where measured.
- **LLM variance / path dependence:** `temp 0.0` `seed 42`; log `model_version`; same prompt across baselines excluding mechanism memory; agent priors decoupling-before-aggregation.
- **Verification tautology:** `_matches` on `postconditions` could be trivially true if postcondition empty. Mitigation: postconditions include `text_contains`/`status` from census; `B-LITERAL` and `NC` leakage checks; deterministic `_matches` not LLM-as-judge; `AUROC` reported.
- **Power:** `n=10` is underpowered for `0.12` delta. Mitigation: disclose power `~0.25`, require Wilson lower bounds and bootstrap CIs; pilot is existence proof for 10-family scale-up, not definitive economics.
- **Cost non-degeneracy:** `B-REPLAY` hit_rate `~0` forced on hold-out makes cost comparison degenerate to `COLD`. Mitigation: also measure `PC1` same-A hit `50 tok` to prove 0-token path exists; report cost ratio only where interpretable; honest f=10 includes distill+retrieval+verification.
- **Compounding errors over 10-15 steps:** task-specific `start_url`/`category`/`product`/`cart` navigation per prior.
- **Jaccard inflation / alias-OOD spurious resolution:** ablate `adopt-any-observed-key` reconstruction per prior; Jaccard >=0.75 constant-anchor prevents E1 hallucination.
- **Immutability:** `normalize` vs raw URL differences; log canonicalization.
- **Kernel gate fabrication:** prior fabricated `sha b8c3f7e1`/`04438d...`; mitigation: require `git diff` non-empty vs `c065bc92...`, `grep` hits, actual `sha256` match claimed, and `audit` recomputation `kernel_has_distill_parameterized true` with zero templates.

## 11. Prereg freeze and raw evidence

Frozen before outcome-bearing B measurement: `request.json`, `spec.json`, `prereg.md`, `freeze.json` hashes; code `src/spider/kernel.py` patch hash; fixtures; thresholds; WebArena-Verified v2 Docker hash `sha256:3e8cb9b945` or static export hash `d652756...`. Deterministic seeds `PYTHONHASHSEED=0` `random.seed 42` `LLM seed 42`. Preserved: `per_task.csv` (task, family, value_A, value_B, baseline, tokens_in/out, calls, latency_ms, success, EXECUTABLE, bound_action, binding_correct, unsubstituted_templates, verification, UNKNOWN, false_accept, ECE_bin, contamination), `registry.json` (slots/templates, `parameter_slots`, `action_template`, `confidence 0.90`), `cost_config.json`, `provenance.json` (commits, run ids, dataset hashes, WebArena census verification, kernel `sha256` + diff + inspection log, unit test output with zero-template verification, `OPENAI_API_KEY` present flag, Playwright version `1.63.0` check, model version, nginx HIT 960/960 and AX 20-sample notes), Playwright traces sampled (`trace.zip` per task if available). `result.json` uses stable metric IDs and `controls` keyed by frozen `PC-PARAM-REGRESSION-AND-LITERAL-HIT`/`NC-SHUFFLED-AND-RANDOM`/`B-COLD`/`B-RAG`/`B-REPLAY-TERX`/`B-INSTR`/`B-LITERAL`; `artifacts` list with `path+sha256` and `role raw|derived`; `observations` distinct from interpretations.

## 12. Consequences

- **If SURVIVES:** `C-PARAM-INHERIT` `EXPERIMENTAL → VALIDATED` at bounded single-family pilot ceiling (first real-LLM multi-param `A→B` transfer beyond `RAG`/`TERX` with calibrated `UNKNOWN` `ECE<=0.15`, zero unsubstituted templates, honest f=10 cost). Unblocks 10-family scale-up and `C-LLM-INHERIT`/`C-RESIDUAL-NOVELTY` economics; authorizes `src/spider/kernel.py` promotion (`promotion_ready true` pending kernel tests and audit `PASS`). No `SHIPPED` — requires `>=10`-family replication and freshness hardening per `research/portfolio/POLICY.md`. Runtime nginx HIT and intel AX dependencies remain advisory.
- **If FALSIFIED / MIXED:** Claim stays `EXPERIMENTAL` (or bounded `REJECTED` for this family setting: parameterized transfer does not beat cold/retrieval/replay/instructions on that family's hold-out). If `MIXED` (binds but no margin), investigate Playwright/verification/agent prompt, not just induction. If no margin vs `RAG`/`REPLAY` where they already miss, inheritance adds no pilot economics; Director should keep next cycle on `C-FRESHNESS`/`C-DELTA-REPAIR`/`C-SEMANTIC-RESOLVE` per portfolio, defer `C-PRODUCT-ECON` scale-up. Either outcome resolves the 42-attempt bottleneck at low cost and prevents premature 10-family spend. Per `AGENTS.md` `UNKNOWN` is valid; do not over-claim to `PRODUCT_CORE` without verdict. Negative still high information: definitively tests kernel fix with zero-template gate and single-family existence proof; if positive, justifies PreAct pivot deferral; if negative, justifies pivot to PreAct state-machine compilation without further slot tuning.
- **If MEASUREMENT_INVALID:** No claim update; status remains `EXPERIMENTAL`. Priority is fixing kernel port (single-prefix, Jaccard >=0.75, field-filter distinct slots) + zero-template verification / census / LLM / verification substrate before re-testing (per `handoff.do_not_assume` and `EXPERIMENT_PACKET s9` infrastructure failure ≠ falsification). `Global Research Director` may pivot Graph to orthogonal question if substrate remains unavailable after provision attempt, per `research/portfolio/POLICY.md`.

## 13. Reproducibility checklist

- [ ] `src/spider/kernel.py` `sha256` and `grep` inspection log (`distill_parameterized`, `_common_prefix_and_suffix`, `Jaccard`, `_is_allowed_path`, `_field_path_to_slot_name`) + `git diff` vs `base_sha c065bc92f8b56ab2ddfdaa0612097ee7fbe7a953` with zero unsubstituted template verification
- [ ] Unit tests `tests/test_kernel_param_inherit.py` `B1/B4/D1/E1/B2/B3/B5/C2` PASS (including `distinct slot per field-path`, `user-4` full-value double-prefix, zero-template check)
- [ ] WebArena-Verified v2 census hash `d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30` + family split + zero-overlap proof `value_set_A ∩ B = ∅` with hashes + duplication CI check
- [ ] Model `gpt-4o-mini-2024-07-18` (or approved haiku/flash) `temp 0.0` `seed 42` + Playwright `chromium` version + `PYTHONHASHSEED=0` + nginx HIT 960/960 and AX 20-sample notes disclosed
- [ ] `freeze.json` hashes before any B measurement
- [ ] `result.json` with stable metric IDs (`M-EXECUTABLE-SPIDER` etc., including `M-UNSUBSTITUTED-TEMPLATES`), `controls` keyed by frozen IDs (`PC-PARAM-REGRESSION-AND-LITERAL-HIT`, `NC-SHUFFLED-AND-RANDOM`, `B-COLD` etc.), `artifacts` with `path+sha256` and `observations` distinct from interpretations
- [ ] `report.md` bounded by `result.json`, `provenance.json` complete with kernel sha256, unit test zero-template log, `OPENAI_API_KEY` flag, Playwright version
- [ ] Audit recomputes `M-EXECUTABLE`, `M-BINDING-CORRECT`, `M-UNSUBSTITUTED-TEMPLATES`, `M-SUCCESS` margins, `M-FALSE-ACCEPT`, `M-ECE` from raw CSV + registry + cost_config
- [ ] No bijective cost proxy; honest `tokens+browser+retrieval+verification` with amortized `f=10` only to SPIDER, `f=1,10,100` reported separately

*Prereg frozen pre-outcome. Any analysis change after seeing B outcomes is exploratory; a new confirmatory claim requires a new prereg and untouched B data. This DESIGN does not run outcome-bearing measurements.*
