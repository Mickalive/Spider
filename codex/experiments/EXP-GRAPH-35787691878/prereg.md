# EXP-GRAPH-35787691878 — Preregistration (Research 2.0 Graph, C-PARAM-INHERIT single-family pilot)

**Lane:** graph · **Claim:** C-PARAM-INHERIT (Mechanisms parameterize to unseen identifiers) · **Mode:** REOPEN (Director mandate SUPERSEDE) · **Status:** DESIGN (pre-freeze)

## 1. Scientific question (Director mandate, binding)

> After genuinely fixing `src/spider/kernel.py` `distill_parameterized` (single-prefix `_common_prefix_and_suffix`, field-path relevance filter `url/body.*/headers.*` only, Jaccard `>=0.75` constant-anchor check, distinct slot per field-path, confidence `0.90`) verified by code inspection/unit tests, does a narrowed family hold-out single-family pilot on WebArena-Verified v2 (train 3–5 exemplars of one family on resource A, test zero-overlap resource B, `>=1` family `>=10` tasks) achieve `EXECUTABLE >=0.75` and binding correctness `>=0.90` with zero unsubstituted templates, success margin `>=0.12` vs each of `B-COLD`/`B-RAG`/`B-REPLAY-TERX`/`B-INSTR`, `false_accept <=0.10` `UNKNOWN` in `[0.00,0.15]` `ECE <=0.15`, with family-stratified/task bootstrap CIs, deterministic `_matches` verification, and honest `tokens+browser+retrieval+verification` cost?

**Inherited parent handoff:** `EXP-GRAPH-35784823623` `MEASUREMENT_INVALID` (0 tasks, kernel not ported `sha256 424c7aac...` 132 lines literal-only, no LLM, no census). Its `next_question` proposed `>=10` families `>=60` tasks requiring distributed infra. Director mandate `REOPEN` `SUPERSEDE`s that scope to the **smallest measurement-ready pilot**: single family `>=10` tasks, no centralized-session-store dependency. This prereg converts the strategic question into a falsifiable single-family pilot.

**Established (must not be re-proven as new):**
- C-PARAM-INHERIT is `EXPERIMENTAL` only at narrow synthetic ceiling: `EXP-PRODUCT-33528829801` audit `PASS` 10/10 single-param common-prefix, and `EXP-PRODUCT-33741671686` audit `PASS` harness-only 21/21 multi-param (not kernel, `run_experiment.py` only, fragile positional mapping).
- WebArena-Verified v2 census `192/49/36` dup `0.9479 [0.9167,0.9792]` exact-copy `0.0781` param_task `0.8958` replicated in `EXP-INTEL-35749371101` audit `PASS` — loadable target, but **not loaded** in parent (`census_verified false`).

**Rejected / do_not_assume:**
- Bijective cost `250+500*10*novelty` and hardcoded 72-task `0.9479` mock are `MEASUREMENT_INVALID` (tautological `rho=1.0`).
- Reported `kernel_check.json` 7-check PASS in parent is rejected as flawed string-match false positive; `src/spider/kernel.py` lacks `distill_parameterized` entirely.
- `MEASUREMENT_INVALID` (0 tasks, missing LLM) is not falsification of parameterized inheritance.

## 2. Hypothesis

`H1`: A corrected `distill_parameterized()` with three fixes — (a) single-prefix `_common_prefix_and_suffix` (common prefix/suffix analysis without double-prefix truncation so `user-4` binds fully), (b) field-path relevance filter restricting `_extract_varying_values` to `url/path`, `body.*`, `headers.*` only (excluding top-level metadata/provenance noise), (c) structure-similarity `Jaccard >=0.75` constant-value anchor to reject pattern-absence hallucination `E1` — with distinct slot naming per field-path and `confidence 0.90`, ported to `src/spider/kernel.py` and verified by inspection + unit tests, will allow 3–5 exemplars of **one** family on resource **A** to induce a mechanism that on never-observed resource **B** (zero value overlap) resolves `EXECUTABLE >=0.75`, binds correctly `>=0.90`, leaves zero `${}` templates, beats each baseline by `>=0.12` success, keeps `false_accept <=0.10` `UNKNOWN [0,0.15]` `ECE <=0.15`.

`H0` (null): Transfer does not exceed baselines; literal/retrieval/replay already capture any `0.9479` duplication that is exact-copy `0.0781`-limited; parameterization adds no margin or violates safety/calibration.

## 3. State, action, target, unit of analysis

- **State representation:** raw `context` dict passed to `resolve()` (preconditions + applicability guards). No hidden site-id leakage; family hold-out ensures test family never seen during distill.
- **Action representation:** `action_template` dict with parameterized slots `${slot}`. Slots named per field-path (`body.sku -> ${sku}` etc.). Binding via `_bind()` on `required_slots | _template_slots`.
- **Target:** Per-task `success` = deterministic postcondition `_matches(mechanism.postconditions, observed_state)` after Playwright execution (not LLM-as-judge). Plus mechanism quality: `EXECUTABLE` rate, `binding_correctness` (bound_action equals gold B identifier), `unsubstituted_templates` count.
- **Unit of analysis:** task. For single-family pilot, family is the block but `n>=10` tasks within one family; bootstrap is task-level (family-block bootstrap collapses to task bootstrap, disclosed). Future 10-family scale-up will use family as block.

## 4. Sampling policy & holdout

- **Dataset:** WebArena-Verified v2 shopping census: load from `data/webarena_verified_v2.json`, `/tmp/webarena`, or verified `https://github.com/web-arena-x/webarena` CSV (3 fetch attempts, hash logged). Dedup by `template+intent` hash as in `EXP-INTEL-35749371101`.
- **Pilot selection:** Choose `>=1` family with `>=10` tasks after dedup. Integer family selection logged (e.g., `family_id=shopping_filter_sku_v2`, tasks 14). Require `>=2` disjoint resource pools `A`/`B` within that family (SKU/store/user IDs). Training uses 3–5 exemplars from **A** only; **B** values have zero exact overlap with **A** for parameterized slots (`value_set_A ∩ B = ∅` verified, logged in `provenance.json`).
- **Holdout:** family hold-out (not random split). Test tasks never seen during distill. Minimum `10` valid tasks required for decision; target `12–20` if budget allows. Claim ceiling bounded to pilot family, not cross-family generalization.
- **Exclusions:** tasks with `>50%` LLM API failure, Playwright timeout `>30s`, or census load failure are excluded and counted; if `<10` valid tasks remain → `MEASUREMENT_INVALID`.
- **Model:** `gpt-4o-mini-2024-07-18` (or approved `haiku`/`flash` equivalent), `temp 0.0`, `seed 42`, `max 15` steps, `4096` tokens, identical Playwright toolset `navigate/click/fill/type/select/goBack/observe` on `chromium` headless, `PYTHONHASHSEED=0`.

## 5. Kernel fixes (what EXECUTE must verify before measuring)

Fixes must be in `src/spider/kernel.py` (graph allowed to patch `src` per Director `REOPEN`), not only harness:

1. `_common_prefix_and_suffix` uses **single-prefix** (common prefix only, no double-prefix that truncates `user-4` → `4`).
2. `_extract_varying_values` field-path filter: allow only `url`, `body.*`, `headers.*` (and `path`); reject top-level `provenance`/`state` noise.
3. `structure_similarity` `Jaccard >=0.75` constant-anchor check to reject `E1` hallucination when values lack common structure.
4. Distinct slot naming per field-path, `confidence 0.90`, stored via registry `parameter_slots` + `action_template` with `required_slots | _template_slots` gating and `_bind` resolution.

**Verification gate before outcome measurement:** code inspection (`grep distill_parameterized/_common_prefix_and_suffix/Jaccard/_is_allowed_path`) + `sha256` logged + unit tests: `B1`/`B4` clean-synthetic regression still pass, `D1` noisy over-param and `E1` hallucination correctly rejected, `B2/B3/B5` short-value and `C2` `user-4` full-value cases. If gate fails → `MEASUREMENT_INVALID`, no claim inference.

## 6. Baselines (strong, same B set, same LLM/tools/verification)

| ID | Mechanism | Cost accounting |
|---|---|---|
| `B-COLD` | Cold LLM, no memory | `LLM tok + browser calls+ms + latency` |
| `B-RAG` | RAG `Jaccard 0.30` retrieval, verbatim replay without slots; `200 tok` retrieval + fallback to COLD on mismatch | measured hit/miss via `_matches` |
| `B-REPLAY-TERX` | 0-token exact replay: exact `action_template` equality → `0 tok +1 verify (50 tok, 90ms)` else fallback to COLD | `hit_rate` expected `~0` on hold-out |
| `B-INSTR` | Hand-authored site instructions, no slots; instruction `200 tok` amortized `200/f` | same verification |
| `B-LITERAL` | Literal `distill()` without slots, exact registry match | confirms param necessity; success `>0.15` signals leakage |

All baselines run on the **identical** pilot B set with identical budget and deterministic `_matches` verification. Costs measured via API `usage` tokens + browser `ms`, not formulas.

## 7. Controls

- **Positive** `PC-PARAM-REGRESSION-AND-LITERAL-HIT`:
  - `PC1` same-A literal hit via `B-REPLAY-TERX`: `hit_rate 1.0`, `cost 50 tok`, `success 1.0`.
  - `PC2` multi-param same-A via `distill_parameterized` on 3–5 A exemplars, same `A` via registry `_bind`/`verify`: `EXECUTABLE 1.0`, `binding 1.0`, `success >=0.90`, zero templates.
  Failure → `MEASUREMENT_INVALID` (substrate broken, not falsification).

- **Null** `NC-SHUFFLED-AND-RANDOM` (through real `bind`/`verify`):
  - `NC1` shuffled slot mapping (permute slots): expected `success <= B-COLD+0.05`, `false_accept >=0.25`, `binding <0.50`.
  - `NC2` random retrieval: expected `false_accept >=0.30` or `success <= B-COLD`.
  If `NC1 success >= SPIDER-0.05` → SPIDER effect spurious.

Stable IDs: `M-SUCCESS-SPIDER`, `M-SUCCESS-COLD`, `M-SUCCESS-RAG`, `M-SUCCESS-REPLAY`, `M-SUCCESS-INSTR`, `M-EXECUTABLE-SPIDER`, `M-BINDING-CORRECT`, `M-UNSUBSTITUTED-TEMPLATES`, `M-FALSE-ACCEPT-SPIDER`, `M-UNKNOWN-RATE`, `ECE`, `M-COST-SPIDER`, `M-COST-COLD`, `M-COST-RAG`, `M-AMORTIZED-SAVING-vs-COLD`, `M-COST-RATIO-RAG`.

## 8. Metrics, uncertainty, and decision rule (frozen)

**Primary metrics on pilot B (real LLM+Playwright, not proxy):**
- `M-EXECUTABLE-SPIDER` (rate `EXECUTABLE` resolutions), Wilson 95% CI.
- `M-BINDING-CORRECT` (correct `bound_action` among `EXECUTABLE`), Wilson 95% CI.
- `M-UNSUBSTITUTED-TEMPLATES` (count of remaining `${}` in `bound_action` among `EXECUTABLE`).
- `M-SUCCESS-*` per baseline, deterministic `_matches`.
- `M-FALSE-ACCEPT` (verification passed but binding wrong / postcondition false), `M-UNKNOWN-RATE` (abstentions), `ECE` (10 bins, confidence vs success), `verification AUROC` where measurable, `contamination <0.10`.

**Uncertainty:** Task bootstrap `5000` resamples `seed 42` (family-block collapses to task bootstrap for single family); Wilson CIs for rates; paired McNemar for success margins where `n` permits. Disclose power: at `n=10`, power to detect `0.12` delta from `0.45` baseline is ~`0.25` (pilot is existence proof, CIs will be wide).

**Adequacy rule:** `>=10` valid B tasks with zero-overlap proof and kernel gate PASS. Otherwise `MEASUREMENT_INVALID`.

**Decision rule:**

`SURVIVES_CURRENT_TEST` requires **all** `C1–C5`:

- `C1` success: `M-SUCCESS-SPIDER >=0.65` and `> B-COLD +0.12` and `> B-RAG +0.12` and `> B-REPLAY +0.12` and `> B-INSTR +0.10`, bootstrap `95%` CI lower `>0.02`, McNemar `p<0.05` where `n` permits.
- `C2` mechanism: `M-EXECUTABLE-SPIDER >=0.75` (Wilson lower `>=0.65`) and `M-BINDING-CORRECT >=0.90` (Wilson lower `>=0.80`) with `M-UNSUBSTITUTED-TEMPLATES =0`.
- `C3` safety: `M-FALSE-ACCEPT-SPIDER <=0.10` and `M-UNKNOWN-RATE in [0.00,0.15]` and `B-LITERAL success <=0.15` on same B.
- `C4` controls: `PC1` `hit_rate 1.0` `50 tok` `success 1.0` PASS and `PC2` `1.0/1.0/>=0.90` PASS; `NC1` `success <= COLD+0.05` and `false_accept >=0.25` and `NC2` `false_accept >=0.30` or `success <= COLD`.
- `C5` calibration: `UNKNOWN` cases have `confidence <0.80` or missing slots, `ECE <=0.15`, `AUROC >=0.75` where measurable, `contamination <0.10`.

Secondary `C6` economics `E-ECON` is **reported** not gating for `SURVIVES` in this pilot: `M-AMORTIZED-SAVING-vs-COLD` at `f=10` and `M-COST-RATIO-RAG` with bootstrap CIs. If `saving >=25%` and `ratio <=0.85` with `CI` not crossing `1.0`, product economics strengthened but not required due to limited `n`.

`FALSIFIED` if any `C1–C3` fails on valid substrate. `MIXED` if `C1` margin fails but `C2` passes (binds but downstream fails → repair investigation). `MEASUREMENT_INVALID` if kernel not ported, `<10` tasks, census not verified, `>50%` LLM failures, or verification broken (substrate failure ≠ falsification).

## 9. Cost accounting (honest, amortized)

Per-task: `cost = LLM input+output tok (API usage) + browser calls+ms + retrieval 200 tok + verification 50 tok + repair 1 step if verification fails`. `distill ~1000 tok` amortized `1000/f` **only** to SPIDER; instruction `200/f` only to `B-INSTR`. Report raw and amortized `f=1,10,100` with bootstrap CIs. Latency = `LLM + browser + retrieval + verification + repair`. Token, browser, latency reported separately. No bijective formula.

## 10. Validity threats and mitigations

- **Ceiling degeneracy:** Pilot family may be trivial (all bodies/HIT-cache discriminate `1.0`). Mitigation: choose family with at least `path+body+headers` variation; require `PC2` multi-param (not single-field) and report per-slot binding.
- **Singleton PMI / template tautology:** not relevant here; binding correctness is deterministic identifier equality, not PMI.
- **Site leakage:** Random split would leak site identity. Mitigation: family hold-out with `value_set` intersection proof `=0`.
- **LLM variance:** `temp 0.0` `seed 42`; log `model_version`; same prompt across baselines excluding mechanism memory.
- **Verification tautology:** `_matches` on `postconditions` could be trivially true if postcondition is empty. Mitigation: postconditions include `text_contains` / `status` from census; `B-LITERAL` and `NC` leakage checks.
- **Power:** `n=10` is underpowered for `0.12` delta. Mitigation: disclose power, require Wilson lower bounds and bootstrap CIs; pilot is existence proof for 10-family scale-up, not definitive economics.
- **Cost non-degeneracy:** `B-REPLAY` hit_rate `~0` forced on hold-out makes cost comparison degenerate to `COLD`. Mitigation: also measure `PC1` same-A hit to prove `0`-token path exists.

## 11. Prereg freeze and raw evidence

Frozen before outcome-bearing measurement: `request.json`, `spec.json`, `prereg.md`, `freeze.json` hashes; code `src/spider/kernel.py` patch hash; fixtures; thresholds. Deterministic seeds `PYTHONHASHSEED=0`. Preserved: `per_task.csv` (task, family, value_A, value_B, baseline, tokens, calls, latency, success, bound_action, verification, UNKNOWN, false_accept), `registry.json` (slots/templates), `cost_config.json`, `provenance.json` (commits, run ids, census hash, kernel `sha256`, `OPENAI_API_KEY` present flag, Playwright version), Playwright traces sampled.

## 12. Consequences

- **If SURVIVES:** `C-PARAM-INHERIT` `EXPERIMENTAL → VALIDATED` at bounded single-family pilot ceiling (first real-LLM multi-param `A→B` transfer beyond `RAG`/`TERX` with calibrated `UNKNOWN`). Unblocks 10-family scale-up and `C-LLM-INHERIT`/`C-RESIDUAL-NOVELTY` economics; authorizes `src/spider/kernel.py` promotion (`promotion_ready true` pending kernel tests). No `SHIPPED` — requires `>=10`-family replication and freshness hardening.
- **If FALSIFIED / MIXED:** Claim stays `EXPERIMENTAL` (or bounded `REJECTED` for this family setting). If binds but no margin, investigate Playwright/verification, not just induction. If no margin vs `RAG`/`REPLAY` where they already miss, inheritance adds no pilot economics; Director should keep next cycle on `C-FRESHNESS`/`C-DELTA-REPAIR`/`C-SEMANTIC-RESOLVE` per portfolio, defer `C-PRODUCT-ECON` scale-up. Either outcome resolves the 42-attempt bottleneck at low cost.
- **If MEASUREMENT_INVALID:** No claim update; priority is fixing kernel port / census / LLM / verification substrate before re-testing (per `handoff.do_not_assume`).

## 13. Reproducibility checklist

- [ ] `src/spider/kernel.py` `sha256` and `grep` inspection log
- [ ] Unit tests `B1/B4/D1/E1/B2/B3/B5/C2` PASS
- [ ] WebArena-Verified v2 census hash + family split + zero-overlap proof
- [ ] Model `gpt-4o-mini-2024-07-18` `temp 0.0` `seed 42` + Playwright `chromium` version
- [ ] `freeze.json` hashes before any B measurement
- [ ] `result.json` with stable metric IDs, `controls` keyed by frozen IDs, `artifacts` with `path+sha256`
- [ ] `report.md` bounded by `result.json`, `provenance.json` complete
- [ ] Audit recomputes `M-EXECUTABLE`, `M-BINDING-CORRECT`, `M-SUCCESS` margins, `false_accept`, `ECE` from raw CSV + registry

*Prereg frozen pre-outcome. Any analysis change after seeing B outcomes is exploratory; a new confirmatory claim requires a new prereg and untouched B data.*
