# EXP-GRAPH-35876306030 Report — Single-Family add_to_cart Pilot (C-PARAM-INHERIT)

**Lane:** graph · **Claim:** C-PARAM-INHERIT · **Status:** MEASUREMENT_INVALID · **Outcome:** NOT_APPLICABLE · **Date:** 2026-09-23 · **Run:** 35876306030

## Executive Summary

Frozen design required (a) durable `src/spider/kernel.py` fix `distill_parameterized` with single-prefix `_common_prefix_and_suffix`, distinct slot per field-path via `_field_path_to_slot_name`/`_sanitize_slot`, field-path filter `url/body.*/headers.*` via `_is_allowed_path`/`_ALLOWED_PREFIXES`, Jaccard `>=0.75` via `_structure_similarity`, confidence `0.90` verified by `grep>=1`, `sha256` HEAD, `git diff base..HEAD` nonempty and `tests/test_kernel_param_inherit.py` passing `B1/B4/D1/E1/C2/B2/B3/B5`, and (b) durable WebArena-Verified v2 census from `data/webarena_verified_v2.json` or Docker `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945` or static export `sha256:d6527566` with `>=10` valid `B` tasks family-stratified zero-overlap (`value_set_A ∩ B = ∅`), then single-family pilot (train 3–5 exemplars resource A, test zero-overlap B) via deterministic `_matches` with `EXECUTABLE>=0.75` (Wilson lower `>=0.65`) and binding `>=0.90` (lower `>=0.80`) zero templates.

**Gate 1 — Kernel:** **FAIL → MEASUREMENT_INVALID.** `src/spider/kernel.py` at HEAD `07a90be2` is 132-line literal-only (`sha256 46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61`), identical to base `9e0898ce`. `grep` 0 hits for all 7 symbols, `git diff base..HEAD -- src/spider/kernel.py` empty (0 bytes), `tests/test_kernel_param_inherit.py` missing, `SpiderKernel` has no attribute `distill_parameterized` (methods `[distill, invalidate, observe, resolve, verify]` only). Prior EXP-GRAPH-35864745180 fix `sha f2b86c98` on head `19daf51f` not retained on current branch `lab2/graph`.

**Gate 2 — Census:** **FAIL → MEASUREMENT_INVALID.** No durable source: `data/webarena_verified_v2.json` absent, `research/experiments/EXP-GRAPH-35876306030/census.json` absent, Docker image not present (only `ghcr.io` proxies), `tasks_valid 0 <10`.

Per frozen `decision_rule` and `measurement_validity` #1–2, no `B` outcome measurement was attempted. **Scientific outcome is NOT_APPLICABLE, not a falsification.** This is the 6th consecutive MEASUREMENT_INVALID on `C-PARAM-INHERIT` (5 prior described in prereg + current), repeating transient-kernel/fabricated-provenance pattern. `LLM unavailable` (`OPENAI_API_KEY absent`) would make `F3/F4` economics `NOT_APPLICABLE` but is secondary to primary kernel/census invalidity.

## 1. Frozen Design & Prerequisites

Director mandate `CONTINUE` on `C-PARAM-INHERIT` (cycle `35875514628`, claim `EXPERIMENTAL`, `base_sha 9e0898ce6a3334f778e85bf5ceae3de61f57a6f3`) supersedes handoff `next_question` drift. Required: durable `distill_parameterized` at `confidence 0.90` with `single-prefix`, `field-path relevance filter`, `Jaccard>=0.75` distinct slots, plus durable census `>=10 B` tasks zero-overlap, then `EXECUTABLE`/`binding` via `src/spider/kernel.py` `required_slots|template_slots/_bind/verify` deterministic `_matches`, `false_accept<=0.10` `UNKNOWN [0.00,0.15]` `ECE<=0.15`, margins `>=0.12` vs `B-COLD/B-RAG/B-REPLAY-TERX/B-INSTR` with `5000`-bootstrap CIs and honest `f=10` amortized cost.

Prereg thresholds frozen: `EXECUTABLE 0.75` lower `0.65`, `binding 0.90` lower `0.80`, `false_accept 0.10`, `UNKNOWN [0.00,0.15]`, `ECE 0.15`, `margin 0.12`, `saving 25%`, `cost ratio 0.85`, `Jaccard 0.75`, `confidence 0.90`, seeds `PYTHONHASHSEED=0 random 42 LLM 42 bootstrap 42`.

## 2. Kernel Fixes Verification (Gate 1)

| Function | Required | Hits | Present |
|----------|----------|------|---------|
| `distill_parameterized` | `>=1` | `0` | ❌ |
| `_common_prefix_and_suffix` single-prefix | `>=1` | `0` | ❌ |
| `_extract_varying_values` field-filter | `>=1` | `0` | ❌ |
| `_structure_similarity` Jaccard | `>=1` | `0` | ❌ |
| `_is_allowed_path` / `_ALLOWED_PREFIXES` | `>=1` | `0` | ❌ |
| `_field_path_to_slot_name` distinct slots | `>=1` | `0` | ❌ |
| `_sanitize_slot` | `>=1` | `0` | ❌ |
| `confidence 0.90` | `>=1` | `0` | ❌ |
| `single-prefix` comment | `>=1` | `0` | ❌ |
| `Jaccard 0.75` | `>=1` | `0` | ❌ |
| `git diff base..HEAD -- src/spider/kernel.py` nonempty | `true` | `0 bytes` | ❌ |
| `tests/test_kernel_param_inherit.py` exists & `B1/B4/D1/E1/C2/B2/B3/B5` pass | `19/19` | `missing` | ❌ |
| `sha256` matches claimed `f2b86c98` | — | `46929b3a` | ❌ |

`Kernel SHA256:` `46929b3a951df48d7f9d1fd850871073c0d91c1868aa117e13d389fe274e8d61` (HEAD `07a90be2`, base `9e0898ce`). `distill_attempt.json` confirms `SpiderKernel` has `no attribute distill_parameterized`, `_matches` self-test `true` but induction absent.

`prove: research/experiments/EXP-GRAPH-35876306030/raw_evidence/kernel_check.json sha 1b8c5dd7`, `distill_attempt.json sha 9c6d7760`, `unit_test_output.json sha 1bed183d`.

**Verdict:** Gate 1 fails → no `B` inference per `prereg §5 step 1`. Fix not durably committed; transient harness copy cannot substitute per `do_not_assume` 9.

## 3. WebArena Census (Gate 2)

- **Primary:** `data/webarena_verified_v2.json` — `exists false` `sha null`
- **Secondary:** `research/experiments/EXP-GRAPH-35876306030/census.json` — `exists false`
- **Docker:** `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945` — not present (`docker images` only `ghcr.io` proxies)
- **Static export:** `sha256:d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30` — not present
- **Tasks:** `0` (`0` templates, duplication `null`, families≥3 `0`)
- **Pilot family:** `add_to_cart` — `A 0` (`[]`) `B 0` (`[]`) zero-overlap `false`

Adequacy gate `>=10` valid `B` tasks required for decision (`7–9` exploratory, `<7` `MEASUREMENT_INVALID`); here `0`. No durable source, no `404` GitHub fallback counted per `spec`.

`prove: census_attempts.json sha 36504502`.

> **Ceiling (if census existed):** Bounded to single-family file-based census with local `url/body/headers` only, no real `DOM/AX`, `history` branching, `multi-channel` — not production `Docker` full-`DOM`. Even a positive would be `VALIDATED`-narrow, not `SHIPPED`.

## 4. Distill & Resolve (Not Executed)

Procedure frozen `§5` required: `kernel.distill_parameterized([Observation_A1..An])` for `n=3–5` `A` exemplars → registry `confidence 0.90` → `resolve(intent, context, params=B_values)` → `required_slots|template_slots` check → `UNKNOWN` if missing/confidence`<0.80` else `_bind` → deterministic `_matches(postconditions, observed_state)`.

**Not executed:** prerequisite gates 1–2 failed. `per_task.csv` 0 rows (`sha 32894a6e`), `registry.json` 0 mechanisms (`sha 3b501b4b`). `_bind`/`_template_slots` existence verified via `distill_attempt.json` (`_matches_exists true`), but induction path not exercised.

## 5. Metrics (Primary Binding Gate — Not Measured)

| Metric | Value | Wilson 95% CI | Threshold | Status |
|--------|-------|---------------|-----------|--------|
| `M-EXECUTABLE-SPIDER` | `null` | `null` | `≥0.75` lower `≥0.65` | `NOT_MEASURED` |
| `M-BINDING-CORRECT` | `null` | `null` | `≥0.90` lower `≥0.80` | `NOT_MEASURED` |
| `M-UNSUBSTITUTED-TEMPLATES` | `null` | — | `0` | `NOT_MEASURED` |
| `M-FALSE-ACCEPT-SPIDER` | `null` | `null` | `≤0.10` upper `≤0.20` | `NOT_MEASURED` |
| `M-UNKNOWN-RATE-SPIDER` | `null` | — | `[0.00,0.15]` | `NOT_MEASURED` |
| `M-ECE` 10 bins | `null` | — | `≤0.15` | `NOT_MEASURED` |
| `M-SUCCESS-LITERAL` | `null` | `null` | `≤0.15` | `NOT_MEASURED` |

All `null` with reason `kernel_gate_failed` / `census_gate_failed`. Diagnostic `tasks_valid 0`, `kernel_sha 46929b3a`, `kernel_gate_pass false`, `census_gate_pass false`.

**Secondary (LLM-available):** `M-SUCCESS-SPIDER/COLD/RAG/REPLAY/INSTR`, `M-SUCCESS-MARGIN`, `M-AMORTIZED-SAVING-vs-COLD`, `M-COST-RATIO-vs-RAG` — `null` `api_key_absent` plus gate failure, per frozen falsifier `LLM unavailability alone does NOT invalidate F1/F2` but here `F1/F2` also invalid.

## 6. Controls & Baselines

| Control | Expected | Observed | Pass |
|---------|----------|----------|------|
| `KERNEL-FIX` durable commit | `7 hits, sha f2b86c98, diff nonempty, 19 tests` | `0 hits, sha 46929b3a, diff empty, file missing` | **FAIL → MEASUREMENT_INVALID** |
| `CENSUS-VERIFICATION` durable file `≥10 B` zero-overlap | `>=10 B` | `0 B, no file, Docker absent` | **FAIL → MEASUREMENT_INVALID** |
| `PC-PARAM-REGRESSION-AND-LITERAL-HIT` PC1 `hit 1.0` PC2 `exec 1.0 bind 1.0` | `PC1 1.0 PC2 1.0` | `null` (gates failed) | `FAIL` (invalid, not falsification) |
| `NC-SHUFFLED-AND-RANDOM` shuffled `<0.50` | `bind <0.50 false_accept >=0.25` | `null` (gates failed) | `FAIL` (invalid) |
| `B-LITERAL` literal `0.0` | `EXECUTABLE 0.0` | `null` (0 tasks) | `FAIL` (invalid) |
| `B-COLD` | `< SPIDER` | `NOT_APPLICABLE` `api_key_absent` | `UNKNOWN` |
| `B-RAG` `TAU 0.30` | `hit 0.05-0.10` | `NOT_APPLICABLE` | `UNKNOWN` |
| `B-REPLAY-TERX` exact | `0.0 on B` | `NOT_APPLICABLE` | `UNKNOWN` |
| `B-INSTR` `200/f` | `< SPIDER` | `NOT_APPLICABLE` | `UNKNOWN` |

All controls exercised via real `src/spider/kernel.py` path where measurable; here they correctly show `FAIL` due to substrate, preserving `RAW→OBSERVATION→MEASUREMENT` distinction.

## 7. Measurement Validity & Threats

- **Kernel gate:** not durable → blocks `B` measurement per `validity #1`. Prior `EXP-GRAPH-35864745180` had `sha f2b86c98` on `19daf51f` but current `lab2/graph` at `07a90be2` lost commit (base `9e0898ce` == HEAD for kernel).
- **Census gate:** no durable source → zero tasks, cannot satisfy `>=10` or `zero_overlap` `SHA256` per `validity #2`.
- **Registry/verify:** `_matches` exists but `_bind` path not exercised due to missing induction; would be `required_slots|template_slots/_bind` + deterministic postcondition.
- **Baselines:** identical `B` set not available; `B-LITERAL` param necessity not testable with 0 tasks.
- **Cost:** honest `API usage + browser + retrieval 200 tok + verification 50 tok + distill 1000/f` only for `SPIDER` when LLM available; here `null`.
- **Statistics:** `Wilson` and `5000`-bootstrap `seed 42` not computed (0 `n`); power disclosure `~0.45` at `n=14` for `0.12` delta remains relevant for future valid run (requires `n>=16` for Wilson lower `0.80` at perfect).
- **Threat:** Single-family file-based ceiling even if valid would be synthetic, not production `Docker` DOM/AX/history.
- **Threat:** `Graph` lane `allowed_code_roots research/harness research/graph` — `src` fix needs product lane or cross-lane commit; this `EXECUTE` correctly does not patch `src` silently, preserving frozen immutability.

## 8. Product Consequences

**Negative:** `MEASUREMENT_INVALID` → `C-PARAM-INHERIT` remains `EXPERIMENTAL` at narrow synthetic ceilings (`EXP-PRODUCT-33528829801` `10/10` single-param audit `PASS`, `EXP-PRODUCT-33741671686` `21/21` harness-only audit `PASS`, `42+` `KERNEL-INTEGRATION-FALSIFIED/PARTIAL`, `6` consecutive `MEASUREMENT_INVALID`). Product **must NOT** promote kernel `distill_parameterized` to `VALIDATED` or `SHIPPED`; `promotion_ready false`.

Next Graph pulse **must NOT** enlarge to `10`-family `60`-task before binding gate passes per Director comparative reasoning (`broad hold-out 5× MEASUREMENT_INVALID with same kernel bugs, lower information per cost`). Next action is fixing durable substrate, not spending LLM budget on `60`-task census.

**If bindings had passed** per `spec` positive consequence: `EXPERIMENTAL → VALIDATED` at bounded single-family file-based ceiling (`one family path+body+headers deterministic _matches zero templates EXECUTABLE>=0.75 binding>=0.90 false_accept<=0.10 UNKNOWN/ECE calibrated distinct slots Jaccard>=0.75`), authorizing `10`-family scale-up and `Docker` full-DOM for `C-LLM-INHERIT`/`C-PRODUCT-ECON` but not immediate `SHIPPED`.

**If valid negative (F1/F2 fail):** would falsify `C-PARAM-INHERIT` for this family despite fix, triggering pivot to orthogonal high-upside (`Intel` within-store, `Frontier` JIT/workflow `O(1)` cost thesis, `Runtime` distributed freshness/shared-store) rather than census enlargement.

## 9. Unresolved & Next Steps

- Whether fixed `distill_parameterized` generalizes `A→B` still unknown — needs durable `src` commit.
- Whether file-based success generalizes to `Docker` production DOM/AX — unknown.
- Whether `LLM` margins `>=0.12` and `saving >=25%` `f=10` `cost ratio <=0.85` hold — `NOT_APPLICABLE`, needs `gpt-4o-mini`/`haiku`/`flash` provision.
- `ECE<=0.15` `false_accept<=0.10` at `n>=16` — no data.
- Wiring of `_common_prefix_and_suffix` `user-4` full-value and `_structure_similarity` threshold — not tested.

**Minimal unblocking actions (smallest next):**

1. Durably commit `src/spider/kernel.py` patch with 7 functions, `confidence 0.90`, `single-prefix` (common prefix only), `_is_allowed_path` `url/body.*/headers.*`, `Jaccard>=0.75`, distinct slot naming, verified by `grep>=1`, `sha256` HEAD, `git diff base_sha..HEAD nonempty` vs `9e0898ce`.
2. Provision durable census: place `data/webarena_verified_v2.json` pre-existing or pull `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945` or verify static export `sha256:d6527566` with pinned hash, `>=10` valid `B` tasks zero-overlap `SHA256`.
3. Restore `tests/test_kernel_param_inherit.py` `19/19` PASS (`B1/B4/D1/E1/C2/B2/B3/B5`) and install `pytest`.
4. Then re-run this exact frozen pilot (5 `A` / 16 `B` `add_to_cart`) via deterministic `_matches`; `LLM` provision optional for economics but not required for binding gate.

## 10. Reproducibility

Frozen inputs (`request.json sha b6b7c45e`, `spec.json sha 1c079eba`, `prereg.md sha 1ec076d2`, `freeze.json sha 3e9173d`) hashed in `freeze.json`; seeds `PYTHONHASHSEED=0 random 42 bootstrap 42`; raw evidence `raw_evidence/*.json/csv` with `SHA256` logged; `provenance.json` with commits (`base 9e0898ce head 07a90be2 pre 364d1c9a`), `kernel sha+grep+diff`, `dataset` hashes, `census` verification log. No post-hoc threshold weakening.

---

*`RAW EVIDENCE → OBSERVATION → DERIVED MEASUREMENT → INTERPRETATION` preserved; `status` describes measurement validity, `outcome` describes scientific answer; infrastructure failure is not scientific falsification per `EXPERIMENT_PACKET s9`.*
