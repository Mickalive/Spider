# EXP-GRAPH-35864745180 preregistration

> After genuinely fixing src/spider/kernel.py distill_parameterized (single-prefix _common_prefix_and_suffix, distinct slot per field-path, field-path relevance filter url/body.*/headers.* only, Jaccard >=0.75 constant-anchor, confidence 0.90) verified by code inspection/unit tests with zero unsubstituted templates, does a narrowed single-family WebArena-Verified v2 pilot (train 3-5 exemplars of one family on resource A, test zero-overlap resource B, >=10 tasks family, family-stratified 5000-bootstrap CIs) achieve EXECUTABLE>=0.75 and binding correctness>=0.90, success margin>=0.12 vs each of B-COLD/B-RAG/B-REPLAY-TERX/B-INSTR, false_accept<=0.10 UNKNOWN in [0.00,0.15] ECE<=0.15, with honest tokens+browser+retrieval+verification cost at f=10?

**Lane:** graph | **Claim:** C-PARAM-INHERIT | **Director mandate:** PIVOT SUPERSEDE (cycle 35864015175) | **Parent handoff:** EXP-GRAPH-35860314278 (BLOCKED) — continuity evidence only, do_not_assume not falsification

---

## 1. Background & prior state

SPIDER has 272 canonical experiments, zero claims at PRODUCT_CORE/SHIPPED. C-PARAM-INHERIT is EXPERIMENTAL at narrow synthetic ceilings only:

- EXP-PRODUCT-33528829801 audit PASS: single-param 10/10 EXECUTABLE, 5.42% synthetic saving, single-field common-prefix heuristic, simulated baselines.
- EXP-PRODUCT-33741671686 audit PASS: harness-only multi-param 21/21 binding (21/21 EXECUTABLE/binding) — **not** kernel-integrated (run_experiment.py only).
- 42+ subsequent attempts: KERNEL-INTEGRATION-FALSIFIED / PARTIAL (double-prefix truncates `user-4`→`4`, relevance filter missing, Jaccard hallucination) and last 5 Graph pilots MEASUREMENT_INVALID: transient kernel patch not persisted (HEAD sha 46929b3a 132 lines literal-only, grep 0 hits distill_parameterized vs claimed 7-check PASS b8c3f7.../04438d...), fabricated provenance, synthetic census mismatch (275 tasks dup 0.8182 vs target 0.9479, 7<10 tasks), 0/60 tasks, LLM keys absent. No durable src/spider/kernel.py fix audited as PASS.

Graph lane is IDLE after 6 consecutive BLOCKED on C-DELTA-REPAIR requiring real LLM+Playwright+nginx HIT/SWR/SIE/304; distributed C-FRESHNESS belongs to Runtime where gunicorn+nginx shared store is being built. Director PIVOT rationale: re-dispatching delta-repair has ~0 expected information gain until runtime delivers shared store; single-family file-based census (36 families >=3, 192 tasks, 49 templates, duplication 0.9479, param_task 0.8958 per EXP-INTEL-35749371101 audit PASS) can isolate executable/binding gate without live LLM, directly unblocking C-LLM-INHERIT/C-PRODUCT-ECON decisions and providing deterministic _matches verification prerequisite.

Parent handoff carry_forward preserved (established: frozen design integrity, infrastructure absence BLOCKED not falsification, simulation fallback resisted, bounded simulation ceiling only 0.833 success but token 0.613>0.50 artefactual, runtime synthetic HIT 960/960, kernel fixes durably in 3c61f9fc claim but not at HEAD; rejected: simulation economics not general falsification; unknown: real LLM repair/token/browser/verification/contamination/byte identity/per-family heterogeneity; do_not_assume: BLOCKED != falsified, simulation PASS != measurement validity, token ratios != real economics, AUROC 1.0 artefactual, contamination hardcoded). New experiment SUPERSEDEs parent question to C-PARAM-INHERIT single-family pilot per Director mandate comparative reasoning: vs CONTINUE delta-repair (same BLOCKED infra, 7th repeat operational failure), vs distributed FRESHNESS co-experiment (duplicates runtime work), vs broad >=60-task family hold-out (higher variance, census noise before single-family gate passes) — single-family pilot is minimal discriminating test that can change promotion decision: if EXECUTABLE/binding fails, economics cannot succeed regardless of freshness.

---

## 2. Hypotheses

**H0 (null):** Corrected induction provides no benefit beyond literal replay/retrieval on unseen identifiers: EXECUTABLE <0.75 or binding correctness <0.90 or unsubstituted templates >0 (slot collision/double-prefix persists), or false_accept >0.10, UNKNOWN outside [0,0.15], ECE>0.15. When LLM available, SPIDER success ≤ max baseline +0.12 or amortized saving <25% vs COLD / cost ratio >0.85 vs RAG.

**H1 (alternative):** Corrected `distill_parameterized()` at confidence 0.90 enables 3–5 exemplars of ONE family on resource A to induce a mechanism that on never-observed B (value_set_A ∩ B = ∅) resolves EXECUTABLE ≥0.75 (Wilson lower ≥0.65) with binding correctness ≥0.90 (lower ≥0.80) and zero unsubstituted `${}` templates via deterministic _matches, with false_accept ≤0.10 UNKNOWN [0,0.15] ECE ≤0.15, and when LLM substrate available, success margin ≥0.12 vs each of B-COLD/B-RAG/B-REPLAY-TERX/B-INSTR (bootstrap CI lower >0.02, McNemar p<0.05) and amortized saving ≥25% vs COLD at f=10 with cost ratio ≤0.85 vs RAG (CI not crossing 1.0).

Expected direction: H1 exceeds H0 on binding gate; LLM success/cost gates exploratory at n=14 but higher power after replication to 60-task multi-family if H1 holds on binding gate.

---

## 3. State / action representation

- **State:** observed DOM/observation.state dict (no hand-authored signature beyond intent+context).
- **Action:** dict with url/path, method, body dict, headers dict (standard HTTP). No browser-only or provenance noise.
- **Preconditions:** exact key equality via `_matches` on context guards (applicability_guards).
- **Parameterization:** `parameter_slots` list + `_template_slots(action_template)`; required_slots = union; distinct slot per field-path via `_field_path_to_slot_name`/`_sanitize_slot`.
- **Confidence:** 0.90 frozen; kernel `min_confidence 0.80` gates EXECUTABLE vs EXPLORE/UNKNOWN.
- **Raw observation preserved:** DOM, action target, browser events, provenance stored separately from derived slots/templates; losses documented in validity notes.

---

## 4. Data

**Census:** WebArena-Verified v2 file-based census. Durable sources only: `data/webarena_verified_v2.json` or Docker `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945` or verified static export `sha256:d65275660814663375028e9017e1f929e3c38321041b125795e2713b52243d30` (successor pinned hash accepted if logged). Raw GitHub 404 fallback alone does not satisfy census_verified. Provenance logs hash, attempt count, source path, duplication stats.

**Pilot family:** `add_to_cart` (template `Add {{sku}} to cart`, 14 tasks: 7 A SKU-A001..A007, 7 B SKU-B001..B007 per synthetic generator; equivalent real family with ≥10 tasks and ≥2 disjoint pools acceptable if deduped and zero-overlap verified). Training: 3–5 exemplars from pool A only. Testing: remaining A (for PC) and all B (≥7) plus any remaining family tasks to reach ≥10 valid B tasks total. Deduplicate by template+intent hash.

**Zero-overlap verification:** value set intersection for all parameterized slots = 0 (sorted value sets SHA256 logged, per-slot and pooled). Example: SKU-A* ∩ SKU-B* = ∅. If any overlap → MEASUREMENT_INVALID.

**Adequacy gate:** ≥10 valid B tasks after dedup/zero-overlap filtering required; 7–9 is downgraded to exploratory (validity note, no VALIDATED promotion); <7 is MEASUREMENT_INVALID. Target 10–14 for this pilot.

**Split:** family hold-out (not random); hold-out family never seen during distill except B pool.

---

## 5. Design & procedure (frozen)

1. **Kernel gate (before any B measurement):** verify `src/spider/kernel.py` durably contains `distill_parameterized`, `_common_prefix_and_suffix` (single-prefix), `_extract_varying_values`, `_structure_similarity`, `_is_allowed_path`/`_ALLOWED_PREFIXES`, `_field_path_to_slot_name`, `_sanitize_slot`; grep hits ≥1, sha256 matches claimed provenance hash, `git diff base_sha..HEAD` nonempty for that file, and `tests/test_kernel_param_inherit.py` exists and passes B1/B4 regression, D1 noisy over-param filtered, E1 hallucination rejected, C2 `user-4` full-value, B2/B3/B5 short values. If any fails → MEASUREMENT_INVALID, no B inference.

2. **Distill:** call `kernel.distill_parameterized([Observation_A1..An])` for n=3–5 A exemplars (action_template-relevant fields only url/path, body.*, headers.*). Registry stores one mechanism per family at confidence 0.90 via actual `registry.all()/write`.

3. **Resolve+bind+verify on B:** for each held-out B task, `resolve(intent, context, params=B_values)` → required_slots check → if missing/confidence <0.80 → UNKNOWN; else `_bind(action_template, params)` → deterministic `_matches(postconditions, observed_state)` against oracle next_state/DOM (not LLM judge). Record EXECUTABLE, binding correctness (oracle bound_action equality), unsubstituted template count (grep `\$\{.*?\}` in bound_action), false_accept, UNKNOWN, confidence.

4. **Baselines on same B set:**
   - B-LITERAL: same pipeline via literal `distill()` (zero-param) → deterministic verify.
   - When LLM available: B-COLD, B-RAG (Jaccard 0.30), B-REPLAY-TERX (exact equality), B-INSTR (200 tok amortized) all with identical model/tools/budget and same deterministic verification. Costs measured live.
   - When LLM unavailable: LLM baselines reported NOT_APPLICABLE.

5. **Controls:** PC1 same-A literal hit (hit_rate 1.0, 50 tok), PC2 same-A multi-param EXECUTABLE 1.0 binding 1.0; NC1 shuffled slot map binding <0.50, NC2 random retrieval false_accept ≥0.30 — all via real registry/_bind/verify.

6. **Costs (LLM-available branch):** per-task LLM tokens (API usage), browser count+ms, retrieval 200 tok, verification 50 tok, repair 1 step, distill ~1000 tok amortized over f=10 only to SPIDER. Task-bootstrap 5000 (seed 42) for CIs. When LLM unavailable, cost metrics null with reason.

All code paths must exercise `src/spider/kernel.py` (graph patched src allowed per Director REOPEN), not harness copy alone.

---

## 6. Metrics

**Primary (binding gate, deterministic, no LLM required):**
- `M-EXECUTABLE-SPIDER` = EXECUTABLE rate on B (Wilson 95% CI).
- `M-BINDING-CORRECT` = binding correctness | EXECUTABLE (oracle equality, Wilson).
- `M-UNSUBSTITUTED-TEMPLATES` = count of `${...}` in EXECUTABLE bound_actions (must be 0).
- `M-FALSE-ACCEPT-SPIDER` = false_accept rate on B (Wilson upper).
- `M-UNKNOWN-RATE-SPIDER` = UNKNOWN rate (must be [0,0.15]).
- `M-ECE` = expected calibration error (10 bins, threshold 0.15).
- `M-BINDING-CONTROL-PC2` etc for controls.

**Secondary (LLM-available, exploratory at n=14):**
- `M-SUCCESS-SPIDER`, `M-SUCCESS-COLD/RAG/REPLAY/INSTR/LITERAL` (deterministic verification success; Wilson + task-bootstrap CI).
- `M-SUCCESS-MARGIN-vs-COLD/RAG/REPLAY/INSTR` (difference, bootstrap CI lower, McNemar p).
- `M-AMORTIZED-SAVING-vs-COLD` at f=10, `M-COST-RATIO-vs-RAG` (bootstrap CI), `M-TOKENS/BROWSER/LATENCY` per task + amortized.

All metric identities stable for EXECUTE/AUDIT/DIRECTOR transmission.

---

## 7. Controls & baselines

**Positive:** PC-PARAM-REGRESSION-AND-LITERAL-HIT — PC1 same-A literal hit_rate 1.0 50 tok success 1.0; PC2 same-A multi-param EXECUTABLE 1.0 binding 1.0 zero templates success ≥0.90 (or binding 1.0 if LLM unavailable). Expected behavior: PC1 1.0, PC2 1.0.

**Null:** NC-SHUFFLED-AND-RANDOM — NC1 shuffled binding <0.50, success ≤ B-COLD, false_accept ≥0.25; NC2 random false_accept ≥0.30 or success ≤ B-COLD. Expected: shuffled/random underperform correct mapping.

**Baseline expectations:** B-LITERAL ~0 EXECUTABLE on held-out B (param necessity); B-COLD success < SPIDER; B-RAG hit ~0.05–0.10 (exact_copy 0.0781); B-REPLAY ~0.0 hit on held-out B; B-INSTR below SPIDER.

Strong baselines per AGENTS.md 13: exact replay, selector/action cache (B-REPLAY), nearest trajectory (B-RAG), workflow/skill (SPIDER), site instructions (B-INSTR).

---

## 8. Decision rule (frozen)

**SURVIVES (binding gate) requires ALL of C1-C3+C5:**
- C1 M-EXECUTABLE-SPIDER ≥0.75 (Wilson lower ≥0.65) and M-BINDING-CORRECT ≥0.90 (lower ≥0.80) and M-UNSUBSTITUTED-TEMPLATES =0.
- C2 M-FALSE-ACCEPT ≤0.10 (upper ≤0.20) and M-UNKNOWN [0,0.15] and B-LITERAL ≤0.15 and PC1/PC2 PASS.
- C3 ECE ≤0.15, verification AUROC ≥0.75 where measurable or contamination <0.10, UNKNOWN cases confidence <0.80 or required_slots missing.
- C5 PC1/PC2 and NC1/NC2 behave as expected (binding <0.50 for shuffled etc).

**FULL SURVIVES (economics) additionally requires C4 when LLM available:**
- C4 M-SUCCESS-SPIDER ≥0.65 and > each of B-COLD/RAG/REPLAY/INSTR by ≥0.12 (COLD/RAG/REPLAY ≥0.12, INSTR ≥0.10) with task-bootstrap 95% CI lower >0.02 and McNemar p<0.05; E-ECON M-AMORTIZED-SAVING ≥25% at f=10 (CI not crossing 1.0) and M-COST-RATIO-RAG ≤0.85 (CI upper <1.0).

FALSIFIED if any C1-C2 fails on valid file-based substrate or (when LLM available) C4 fails. MIXED if C1 passes but C4 fails (LLM available). MEASUREMENT_INVALID if kernel not durably committed, <10 B tasks, census not durably verified, verification broken, or (for C4 only) LLM unavailable — then C4 reported NOT_APPLICABLE/exploratory and primary C1-C3 binding verdict remains valid high-information per Director mandate (single-family pilot can falsify binding without LLM).

Single primary outcome is C1 EXECUTABLE/binding + zero templates; secondary outcome is C4 success margin+economics when LLM present.

---

## 9. Positive / null controls detail

See §7. Controls are executed via real `src/spider/kernel.py` registry/_bind/verify path with deterministic verification, not forced constants. They must show expected pass/fail pattern; inverted controls trigger MEASUREMENT_INVALID or spurious-effect downgrade.

---

## 10. Measurement validity & threats

- **Representation loss:** kernel field-path filter excludes provenance/state noise by design; losses disclosed and tested via D1 noisy case. DOM/a11y tree not required for this file-based gate but disclosed as bounded to synthetic/file census.
- **Leakage:** family hold-out + value_set_A ∩ B = ∅ prevents site identity leakage; trajectory-grouped bootstrap not needed for single-family (task is unit) but task-bootstrap 5000 used.
- **Target integrity:** no predictor contains target; `_matches` uses post-state only after binding; preprocessing fit on TRAIN only (A pool).
- **Sampling integrity:** deterministic seeds (PYTHONHASHSEED=0, random 42, LLM 42, bootstrap 42); policy explicitly described; census dedup prevents duplication inflation (0.9479 logged).
- **Uncertainty integrity:** Wilson CIs for rates, task-bootstrap (5000) for differences/costs with task as unit (not correlated transitions as independent); no injected Gaussian jitter.
- **Power:** at n=10–14, power for 0.12 success delta is ~0.45 — binding gate is primary at this n; economics at this n is exploratory and requires 60-task replication for full power (disclosed).
- **Cost validity:** bijective `250+500*10*novelty` rejected; honest API usage + browser count+ms only when LLM available; otherwise cost null.

---

## 11. Product consequences

**If SURVIVES (binding) or FULL SURVIVES:** advance C-PARAM-INHERIT from EXPERIMENTAL narrow synthetic to VALIDATED at bounded single-family file-based ceiling (one family path+body+headers, deterministic verification, zero templates). Durable src fix justified; authorize promotion_ready true pending kernel tests. Unblocks scale-up to 10-family 60-task and Docker full-DOM hosting for C-LLM-INHERIT/C-PRODUCT-ECON. No immediate SHIPPED.

**If FALSIFIED on binding:** C-PARAM-INHERIT remains EXPERIMENTAL (multi-param real transfer falsified for this family/setting despite durable src fix). Graph next pulse pivots to orthogonal high-upside (Intel within-store, Frontier workflow, Runtime distributed) rather than enlarging to 60 tasks before binding passes. Kernel promotion blocked.

**If MIXED (binds but no LLM margin):** investigate Playwright/agent prompt, not just induction.

**If MEASUREMENT_INVALID:** fix durable src integration (single-prefix, field-filter url/body.*/headers.* only, Jaccard ≥0.75 distinct slots) + file-based census via Docker/static export before re-testing economics; LLM absence alone preserves binding information.

---

## 12. Estimated cost & information gain

File-based pilot without LLM: ~0 API, ~5 min wall-clock. With LLM optional: $3–$7 for 10–14 B tasks ×5 conditions (50–70) + PCs/NCs; 15–25 min. Storage: per-task CSV ~91 rows + registry + census log + kernel sha/diff + provenance.

Expected information gain: HIGH — first durable valid test of central promise after 42+ failed kernel integrations and 5 transient-provenance MEASUREMENT_INVALID pilots; isolates binding prerequisite that can FALSIFY centralized parameterization before 60-task spend, resolving starved-claim bottleneck and tunnel flags with minimal cost.

---

## 13. Reproducibility

Frozen inputs hashed (request.json, spec.json, prereg.md, pilot_family.json, src/spider/kernel.py patch, census hash) in freeze.json. Seeds deterministic. Raw evidence preserved: per-task CSV, registry JSON, cost_config, census verification log, kernel grep/diff/sha, provenance.json with commits/run ids/dataset hashes. Artifacts paths + SHA256 logged. No LLM proxy if LLM unavailable — report null with reason.

---

## 14. Prereg freeze attestation

This prereg is frozen before any outcome-bearing measurement on held-out B. Any change after seeing B outcomes is exploratory and requires new prereg + untouched evidence. Kernel gate verified before B measurement; census zero-overlap verified before distill.

