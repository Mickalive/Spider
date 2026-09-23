# EXP-GRAPH-35918640311 preregistration

> After durably committing src/spider/kernel.py distill_parameterized (single-prefix _common_prefix_and_suffix, distinct slot per field-path via _field_path_to_slot_name/_sanitize_slot, field-path relevance filter url/body.*/headers.* only via _is_allowed_path, Jaccard>=0.75 constant-anchor via _structure_similarity, confidence 0.90) verified by grep>=1, sha256 HEAD, git diff base..HEAD nonempty and tests/test_kernel_param_inherit.py passing B1/B4/D1/E1/C2/B2/B3/B5, and loading WebArena-Verified v2 census from durable source (data/webarena_verified_v2.json or Docker am1n3e/webarena-verified-shopping@sha256:3e8cb9b945 with pinned 64-char hash) with >=10 valid B tasks family-stratified zero-overlap (value_set_A intersect B = empty), does single-family add_to_cart pilot (train 3-5 exemplars resource A, test zero-overlap B) achieve EXECUTABLE>=0.75 (Wilson lower>=0.65) and binding correctness>=0.90 (lower>=0.80) with zero unsubstituted ${} templates via deterministic _matches, false_accept<=0.10 UNKNOWN in [0.00,0.15] ECE<=0.15, success margin>=0.12 vs each of B-COLD/B-RAG/B-REPLAY-TERX/B-INSTR with family-stratified 5000-bootstrap CIs and honest tokens+browser+retrieval+verification amortized cost at f=10?

**Lane:** graph | **Claim:** C-PARAM-INHERIT | **Director mandate:** REOPEN (cycle 35918260262) — binding target C-PARAM-INHERIT | **Parent handoff:** EXP-GRAPH-35880048129 handoff.json sha256 7e120ac7b78fee55ed3059949258fe2163c15fa85ea758f1e97ee48cbbef2b73 — continuity evidence only, disposition SUPERSEDE (binding question is Director's param-inherit pilot, NOT parent's C-FRESHNESS shared-store retest)

---

## 1. Background & prior state

SPIDER has ~298 canonical experiments, zero claims at PRODUCT_CORE/SHIPPED. C-PARAM-INHERIT is EXPERIMENTAL at narrow synthetic ceilings only:

- EXP-PRODUCT-33528829801 audit PASS: single-param 10/10 EXECUTABLE, 5.42% synthetic saving, single-field common-prefix heuristic, simulated baselines, confidence 0.5→0.8.
- EXP-PRODUCT-33741671686 audit PASS: harness-only multi-param 21/21 binding — **not** kernel-integrated (run_experiment.py only, not src/spider/kernel.py).
- 42+ subsequent attempts: KERNEL-INTEGRATION-FALSIFIED / PARTIAL (double-prefix truncates `user-4`→`4`, relevance filter missing, Jaccard hallucination, slot collision) and last 6 Graph pilots MEASUREMENT_INVALID: transient kernel patch not persisted (HEAD 132 lines literal-only, sha 46929b3a vs claimed f2b86c98/19daf51f, grep 0 hits distill_parameterized, test file absent, git diff base_sha..HEAD empty), fabricated provenance, synthetic census mismatch (282 tasks dup 0.8227 vs target duplication 0.9479 exact_copy 0.0781, 44 families, generated on-the-fly by generate_census() not durable source), LLM keys absent. Last audited HEAD 07a90be2 46929b3a (132 lines) has methods [distill, invalidate, observe, resolve, verify] only. No durable src/spider/kernel.py fix audited as PASS since 33528829801.

Graph lane state: IDLE, last_verdict MEASUREMENT_INVALID (EXP-GRAPH-35880048129 was C-FRESHNESS nginx timeout n=0), active_experiment now EXP-GRAPH-35918640311 per state.json.

**Parent handoff carry_forward preserved (SUPERSEDE — advisory only, Director mandate is binding):**

The parent handoff EXP-GRAPH-35880048129 concerns C-FRESHNESS distributed freshness (gunicorn 23.0.0 2x sync + nginx 1.24.0 shared SQLite WAL, C1 TN 0.667 session_status 0.0, stratified r -0.038 TOST p2e-08). Under AGENTS.md precedence and request.json director_mandate.parent_handoff_disposition SUPERSEDE, its `next_question` (re-repair gunicorn+nginx+WAL and retest C-FRESHNESS TN>=0.85) does **not** determine this experiment. It is preserved as continuity evidence but does not override the Director's REOPEN on C-PARAM-INHERIT. Cross-lane dependency is explicit: Runtime owns distributed HS256 store hardening.

- `established` (6 items, C-FRESHNESS scoped — not assumed to imply C-PARAM-INHERIT readiness):
  1. C-FRESHNESS orthogonality at delta=0.15 CONFIRMED on LOCAL single-node Flask HS256 (r=0.0584 CI upper 0.125 TOST PASS n844) and stochastic LOCAL (r=0.0463) — headers-only structural signal orthogonal to behavioral signal when co-occurring.
  2. C-FRESHNESS correlation CONFIRMED on distributed 2-node per-node SQLite (r=-0.0381 CI upper 0.029 TOST p2e-08 n844) — correlation survives distribution.
  3. HS256 symmetric JWT with shared TESTBED_SECRET resolves token cross-node validation (TP=1.0) — prior RS256 bug fixed.
  4. C-FRESHNESS FALSIFIED per frozen C1-C7 on per-node distributed (TN=0.6667 <0.85, session_status 0.0) — stateless round-robin without shared store insufficient.
  5. Behavioral positive control TP=1.0 and confound |r|=0.912 — pipeline sensitivity proven.
  6. No new evidence from EXP-GRAPH-35880048129 (MEASUREMENT_INVALID n=0).
- `rejected` (8 items, C-FRESHNESS scoped):
  Stateless round-robin without shared store sufficient for CONFIRMED; simple-pooled r; RS256 per-process keys; HTTP caching as common cause; body-inclusive structural signals; etc. — none imply C-PARAM-INHERIT rejected.
- `unknown` (6 items — C-FRESHNESS shared-store question remains open but is Runtime's mandate, not this experiment):
  1. Whether shared Redis/SQLite WAL rescues C1 TN>=0.85 while preserving stratified r in [-0.15,0.15] — untested (n=0).
  2. Whether nginx timeout is transient config error.
  3. Whether shared store couples signals.
  4. Generalization beyond Flask localhost.
  5. Whether sticky affinity provides alternative rescue.
  6. Whether delta=0.10 achievable at n>=1200.
- `do_not_assume` (8 items preserved and extended):
  1. MEASUREMENT_INVALID equals falsification — it is infrastructure failure, not evidence against correlation.
  2. Orthogonality falsified — C3/C4 decisively PASS.
  3. Shared store trivially fixes session non-replication without verification.
  4. Single shared-store CONFIRMED implies VALIDATED/PRODUCT_CORE.
  5. C1 failure applies to all endpoints — only session_status fails.
  6. Successful nginx launch implies correct 304 behavior.
  7. Synthetic single-param ceilings imply distributed freshness readiness — separate claim with independent gates (Director explicitly states parent handoff would duplicate Runtime charter and re-block on same substrate; single-family pilot has higher marginal value independent of distributed store).
  8. Runtime status-free r=0.721 falsification implies header-only will also fail.

**Director mandate comparative reasoning (binding, supersedes handoff next_question):**

- Vs parent handoff (repair gunicorn+nginx+WAL and retest C-FRESHNESS TN>=0.85) which duplicates Runtime charter and would re-block on same substrate that caused 0.667 TN; versus C-DELTA-REPAIR localized repair which requires byte-preserving HIT-cache plus gpt-4o-mini Playwright and is BLOCKED until Runtime publishes HIT-cache harness; versus C-FRESHNESS orthogonality which is valid but sequenced after Runtime. Single-family pilot has higher marginal value now: independent of distributed session replication, directly addresses repeated 7-measure kernel fix failures, and unblocks Product/Graph downstream only if it survives — Director rationale verbatim.
- Vs broad family hold-out (>=10 families >=60 tasks) that produced 5 MEASUREMENT_INVALID in a row with same kernel bugs and inflated scope — lower information per cost → rejected.
- Single-family pilot is smallest high-information experiment that can change claim/product decision per AGENTS.md work discipline; avoids repeating broad 49-template census that repeatedly failed with same Jaccard/slot bugs.

**Director agent priors used (priors, not SPIDER evidence — explicitly distinguished):**

- Path dependence / local-optima salience, measurement validity must precede economics (degenerate bootstrap CI [1.0,1.0] and bijective cost make Pareto uninterpretable; honest counters with |rho_shuffled|<0.20 are prerequisite), workflow compilation / hierarchical caching often outperforms flat RAG (13x caching, TVCache — informing Stagehand/TTL pivot), long-horizon compounding error 15-step Playwright hash-truncated DOM, UNKNOWN calibration requires exposure to real failure (mea auditor 0.15 false_accept mock). All distinguished from SPIDER evidence per portfolio ASSESSMENT; tested as falsifiable gates in this experiment.

---

## 2. Hypotheses

**H0 (null):** Corrected induction provides no benefit beyond literal replay/retrieval on unseen identifiers: EXECUTABLE <0.75 or binding correctness <0.90 or unsubstituted templates >0 (slot collision/double-prefix persists), or false_accept >0.10, UNKNOWN outside [0,0.15], ECE>0.15. When LLM available, SPIDER success ≤ max baseline +0.12 or amortized saving <25% vs COLD / cost ratio >0.85 vs RAG. Work-compression limited by h~8% routine ceiling.

**H1 (alternative):** Corrected `distill_parameterized()` at confidence 0.90 enables 3–5 exemplars of ONE family (add_to_cart) on resource A to induce a mechanism that on never-observed B (value_set_A intersect B = empty, family hold-out) resolves EXECUTABLE ≥0.75 (Wilson lower ≥0.65) with binding correctness ≥0.90 (lower ≥0.80) and zero unsubstituted `${}` templates via deterministic _matches, with false_accept ≤0.10 UNKNOWN [0,0.15] ECE ≤0.15, and when LLM substrate available, success margin ≥0.12 vs each of B-COLD/B-RAG/B-REPLAY-TERX/B-INSTR (family-stratified 5000-bootstrap CI lower >0.02, McNemar p<0.05) and amortized saving ≥25% vs COLD at f=10 with cost ratio ≤0.85 vs RAG (CI not crossing 1.0). Distinct slot per field-path, single-prefix, field-path filter url/body.*/headers.* only, Jaccard>=0.75 constant-anchor are sufficient; tool-level compilation with pre/postconditions overcomes per-step retrieval ceiling.

Expected direction: H1 exceeds H0 on binding gate; LLM success/cost gates exploratory at n=14 (power ~0.45 for 0.12 delta) but binding gate alone is discriminating per Director mandate.

---

## 3. State / action representation

- **State:** observed DOM/observation.state dict (no hand-authored signature beyond intent+context). Raw DOM, accessibility tree, browser events, provenance stored separately from derived slots/templates; losses documented.
- **Action:** dict with url/path, method, body dict, headers dict (standard HTTP). No browser-only or provenance noise mixed into action template-relevant paths.
- **Preconditions:** exact key equality via `_matches` on context guards (applicability_guards).
- **Parameterization:** `parameter_slots` list + `_template_slots(action_template)`; required_slots = union; distinct slot per field-path via `_field_path_to_slot_name`/`_sanitize_slot` (e.g., body.sku→sku, headers.X-Csrf-Token→x_csrf_token, url segment→resource_id).
- **Structure similarity:** `_structure_similarity` Jaccard >=0.75 constant-anchor rejects pattern-absence hallucination (E1).
- **Field-path filter:** `_is_allowed_path` / `_ALLOWED_PREFIXES` restricts `_extract_varying_values` to url/path, body.*, headers.* only.
- **Prefix handling:** `_common_prefix_and_suffix` single-prefix (common prefix only, not double-prefix truncation) preserves full values like SKU-B001 / user-4.
- **Confidence:** 0.90 frozen; kernel `min_confidence 0.80` gates EXECUTABLE vs EXPLORE/UNKNOWN.
- **Verification:** deterministic `_matches` on postconditions vs observed next_state/DOM after `_bind`, not LLM-as-judge.

---

## 4. Data

**Census:** WebArena-Verified v2 file-based census. Durable sources only: `data/webarena_verified_v2.json` (pre-existing, must exist before freeze, not generated on-the-fly) or Docker `am1n3e/webarena-verified-shopping@sha256:3e8cb9b945` with pinned full 64-char hash or verified static export with pinned hash if logged with successor hash. Raw GitHub 404 fallback alone does not satisfy census_verified. Provenance logs hash, attempt count, source path, duplication stats, family counts. Base sha for diff is 98b40ef4df6bac37548b4dbbbd823ccceaed35a1 (from request.json).

**Pilot family:** `add_to_cart` (template `Add {{sku}} to cart`, 14 tasks: 7 A SKU-A001..A007, 7 B SKU-B001..B007 per synthetic generator; equivalent real family with ≥10 tasks and ≥2 disjoint pools acceptable if deduped and zero-overlap verified). Training: 3–5 exemplars from pool A only. Testing: remaining A (for PC) and all B (≥7) plus any remaining family tasks to reach ≥10 valid B tasks total. Deduplicate by template+intent hash.

**Zero-overlap verification:** value set intersection for all parameterized slots = 0 (sorted value sets SHA256 logged, per-slot and pooled). Example: SKU-A* ∩ SKU-B* = ∅. If any overlap → MEASUREMENT_INVALID. Logged as SHA256 of sorted value sets.

**Adequacy gate:** ≥10 valid B tasks after dedup/zero-overlap filtering required for decision; 7–9 downgraded to exploratory (validity note, no VALIDATED promotion); <7 MEASUREMENT_INVALID. Target 10–16 for this pilot (Wilson half-width ~0.22 at 10).

**Split:** family hold-out (not random); hold-out family never seen during distill except B pool. Family-stratified bootstrap terminology retained for downstream scale-up; task is unit for single-family.

---

## 5. Design & procedure (frozen)

1. **Kernel gate (before any B measurement):** verify `src/spider/kernel.py` durably contains `distill_parameterized`, `_common_prefix_and_suffix` (single-prefix), `_extract_varying_values`, `_structure_similarity`, `_is_allowed_path`/`_ALLOWED_PREFIXES`, `_field_path_to_slot_name`, `_sanitize_slot`; grep hits ≥1 each, sha256 matches claimed provenance hash AND matches HEAD, `git diff base_sha 98b40ef4df6bac37548b4dbbbd823ccceaed35a1..HEAD` nonempty for that file, and `tests/test_kernel_param_inherit.py` exists and passes B1/B4 regression, D1 noisy over-param filtered, E1 hallucination rejected, C2 `user-4` full-value, B2/B3/B5 short values. If any fails → MEASUREMENT_INVALID, no B inference. No outcome-bearing B measurement until gate passes.

2. **Distill:** call `kernel.distill_parameterized([Observation_A1..An])` for n=3–5 A exemplars (action_template-relevant fields only url/path, body.*, headers.*). Registry stores one mechanism per family at confidence 0.90 via actual `registry.all()/write`. Mechanism logged with slots/templates.

3. **Resolve+bind+verify on B:** for each held-out B task, `resolve(intent, context, params=B_values)` → required_slots check → if missing/confidence <0.80 → UNKNOWN; else `_bind(action_template, params)` → deterministic `_matches(postconditions, observed_state)` against oracle next_state/DOM (not LLM judge). Record EXECUTABLE, binding correctness (oracle bound_action equality), unsubstituted template count (grep `\$\{.*?\}` in bound_action), false_accept, UNKNOWN, confidence, ECE bins.

4. **Baselines on same B set:**
   - B-LITERAL: same pipeline via literal `distill()` (zero-param) → deterministic verify.
   - When LLM available: B-COLD, B-RAG (Jaccard 0.30), B-REPLAY-TERX (exact action_template string equality), B-INSTR (200 tok amortized as 200/f) all with identical model/tools/budget (gpt-4o-mini-2024-07-18 or approved haiku/flash, temp 0.0, seed 42, max 15 steps, 4096 tokens, Playwright chromium headless) and same deterministic verification. Costs measured live (API usage, browser count+ms).
   - When LLM unavailable: LLM baselines reported NOT_APPLICABLE (not zero) per falsifier.

5. **Controls:** PC1 same-A literal hit (hit_rate 1.0, 50 tok), PC2 same-A multi-param EXECUTABLE 1.0 binding 1.0 (success ≥0.90 if LLM available else binding 1.0 suffices); NC1 shuffled slot map binding <0.50, NC2 random retrieval false_accept ≥0.30 — all via real registry/_bind/verify with actual costs.

6. **Costs (LLM-available branch):** per-task LLM tokens (API usage), browser count+ms, retrieval 200 tok, verification 50 tok, repair 1 step, distill ~1000 tok amortized over f=10 only to SPIDER. Family-stratified task-bootstrap 5000 (seed 42) for CIs on cost ratios/success differences. When LLM unavailable, cost metrics null with reason api_key_absent and binding gate remains valid.

All code paths must exercise `src/spider/kernel.py` (graph allowed_code_roots: research/harness, research/graph; Product scope src/tests/sdk but kernel fix must be durable in src), not harness copy alone. Harness may call kernel but must verify via sha256+diff.

---

## 6. Metrics

**Primary (binding gate, deterministic, no LLM required) — stable identities for EXECUTE/AUDIT/DIRECTOR:**

- `M-EXECUTABLE-SPIDER` = EXECUTABLE rate on B (Wilson 95% CI, task as unit).
- `M-BINDING-CORRECT` = binding correctness | EXECUTABLE (oracle equality, Wilson 95% CI).
- `M-UNSUBSTITUTED-TEMPLATES` = count of `${...}` in EXECUTABLE bound_actions (must be 0).
- `M-FALSE-ACCEPT-SPIDER` = false_accept rate on B (Wilson upper).
- `M-UNKNOWN-RATE-SPIDER` = UNKNOWN rate (must be [0.00,0.15]).
- `M-ECE` = expected calibration error (10 bins, threshold 0.15).
- `M-SUCCESS-LITERAL` (B-LITERAL) EXECUTABLE/success on same B (must ≤0.15).
- `M-BINDING-CONTROL-PC2`, `M-PC1-HIT-RATE` etc for controls.

**Secondary (LLM-available, exploratory at n=14 — 5000-bootstrap CIs):**

- `M-SUCCESS-SPIDER`, `M-SUCCESS-COLD/RAG/REPLAY/INSTR/LITERAL` (deterministic verification success; Wilson + task-bootstrap CI).
- `M-SUCCESS-MARGIN-vs-COLD/RAG/REPLAY/INSTR` (difference, bootstrap CI lower, McNemar p).
- `M-AMORTIZED-SAVING-vs-COLD` at f=10, `M-COST-RATIO-vs-RAG` (bootstrap CI), `M-TOKENS/BROWSER/LATENCY` per task + amortized f=1,10,100.
- `M-AMORTIZED-COST-SPIDER` etc with distill 1000 tok / f added only to SPIDER.

All metric identities stable per EXPERIMENT_PACKET; values explicit with units where relevant. When LLM unavailable, LLM metrics null with reason `api_key_absent`.

---

## 7. Controls & baselines

**Positive: PC-PARAM-REGRESSION-AND-LITERAL-HIT** — PC1 same-A literal hit_rate 1.0 50 tok success 1.0; PC2 same-A multi-param EXECUTABLE 1.0 binding 1.0 zero templates success ≥0.90 (or binding 1.0 if LLM unavailable). Expected behavior: PC1 1.0, PC2 1.0. Uses measured verification, not forced constants. Failure → MEASUREMENT_INVALID.

**Null: NC-SHUFFLED-AND-RANDOM** — NC1 shuffled binding <0.50, success ≤ B-COLD, false_accept ≥0.25; NC2 random false_accept ≥0.30 or success ≤ B-COLD. Expected: shuffled/random underperform correct mapping. Both go through actual binding/verification so they CAN fail expected pattern if mapping truly matters (not guaranteed flat). If NC1 success ≥ SPIDER -0.05 on deterministic binding gate, effect spurious.

**Baseline expectations:** B-LITERAL ~0 EXECUTABLE on held-out B (param necessity); B-COLD success < SPIDER; B-RAG hit ~0.05–0.10 (exact_copy 0.0781 vs duplication 0.9479); B-REPLAY ~0.0 hit on held-out B; B-INSTR below SPIDER. Strong baselines per AGENTS.md 13: exact replay (B-REPLAY-TERX), selector/action cache, nearest trajectory (B-RAG), workflow/skill (SPIDER), site instructions (B-INSTR). Memory beating no memory is not enough — SPIDER must beat RAG and replay where replay misses.

---

## 8. Decision rule (frozen)

**SURVIVES_CURRENT_TEST (binding gate) requires ALL of C1-C3+C5** measured via deterministic _matches verification on durable file-based single-family census (not proxy):

- C1: M-EXECUTABLE-SPIDER ≥0.75 (Wilson 95% lower ≥0.65) and M-BINDING-CORRECT ≥0.90 (Wilson lower ≥0.80) among EXECUTABLE with M-UNSUBSTITUTED-TEMPLATES =0 (no ${} remains) — primary discriminating gate.
- C2: safety S-SAFETY: M-FALSE-ACCEPT-SPIDER ≤0.10 (Wilson upper ≤0.20) and M-UNKNOWN-RATE-SPIDER in [0.00,0.15] on valid B and B-LITERAL success ≤0.15 on same B (param necessity) and PC expectations validated.
- C3: calibration: UNKNOWN cases have confidence <0.80 or required_slots missing where applicable, ECE ≤0.15 with 10 bins, verification AUROC ≥0.75 where measurable or contamination <0.10 via unrelated mechanisms.
- C5: controls: PC1 same-A literal hit_rate 1.0 cost 50 tok success 1.0 PASS and PC2 multi-param same-A EXECUTABLE 1.0 binding 1.0 zero templates success ≥0.90 if LLM available else binding 1.0 suffices PASS; NC1 shuffled binding correctness <0.50 and NC2 random false_accept ≥0.30 or success ≤ B-COLD when measured.

**FULL SURVIVES (economics) additionally requires (C4) when LLM available:** M-SUCCESS-SPIDER ≥0.65 and > B-COLD by ≥0.12 and > B-RAG by ≥0.12 and > B-REPLAY-TERX by ≥0.12 and > B-INSTR by ≥0.10 with task-bootstrap 5000 95% CI lower >0.02 and McNemar p<0.05, and E-ECON: M-AMORTIZED-SAVING-SPIDER-vs-COLD ≥25% at f=10 (cost per success) with bootstrap CI not crossing 1.0 and M-COST-RATIO-vs-RAG ≤0.85 with CI upper <1.0. Includes honest tokens+browser+retrieval+verification at f=10 amortized.

FALSIFIED if any C1-C2 fails on valid file-based substrate (excluding PC/NC substrate failures which are MEASUREMENT_INVALID) or if LLM available and C4 fails (no margin or no economics). MIXED if C1 passes but C4 fails when LLM available (binds correctly but agent fails downstream). MEASUREMENT_INVALID if: kernel not durably committed, <10 valid B tasks after dedup/zero-overlap, census not durably verified (404 fallback alone), verification broken, or LLM-dependent C4 alone fails due to api_key_absent — then C4 is NOT_APPLICABLE/exploratory per falsifier and primary C1-C3 binding verdict remains valid high-information per Director mandate comparative reasoning (single-family pilot can falsify binding without LLM). Power disclosure: at n=10–14, power for 0.12 success delta ~0.45, so economics at this n is exploratory; replication to 60-task multi-family required for full power.

Single primary outcome is C1 EXECUTABLE/binding + zero templates; secondary is C4 success margin+economics when LLM present. No post-hoc threshold change.

---

## 9. Positive / null controls detail

See §7. Controls are executed via real `src/spider/kernel.py` registry/_bind/verify path with deterministic verification, not forced constants. They must show expected pass/fail pattern; inverted controls trigger MEASUREMENT_INVALID or spurious-effect downgrade per audit. PC1 validates deterministic verification and 0-cost measurement; PC2 validates induction before generalization. NC1/NC2 prove transfer requires correct parameterization vs task difficulty confound; shuffled mapping must underperform (binding <0.50) to claim parameterization matters.

Strong nulls per AGENTS.md appropriate to claim: literal replay, nearest trajectory, verification gating.

---

## 10. Measurement validity & threats

- **Representation loss:** kernel field-path filter excludes provenance/state noise by design; losses disclosed and tested via D1 noisy case (non-allowed paths filtered). DOM/a11y tree not required for this file-based gate but disclosed as bounded to synthetic/file census (no production DOM/AX/history branching/multi-channel) — claim ceiling explicitly file-based.
- **Leakage:** family hold-out + value_set_A intersect B = empty prevents site identity leakage; trajectory-grouped bootstrap not needed for single-family (task is unit) but task-bootstrap 5000 used for CIs; dedup by template+intent hash prevents duplication inflation (0.9479 logged but not gating).
- **Target integrity:** no predictor contains target; `_matches` uses post-state only after binding; preprocessing fit on TRAIN only (A pool); intent never leaks B values.
- **Sampling integrity:** deterministic seeds (PYTHONHASHSEED=0, random 42, LLM 42 if used, bootstrap 42); policy explicitly described; census dedup prevents inflation; PC/NC not fit on test.
- **Uncertainty integrity:** Wilson CIs for rates, task-bootstrap (5000) for differences/costs with task as unit (not correlated transitions as independent); no injected Gaussian jitter; no degenerate Spearman with ties.
- **Power:** at n=10–14, power for 0.12 success delta ~0.45 — binding gate is primary at this n; economics exploratory and requires 60-task replication for full power (disclosed). Binding gate requires Wilson lower thresholds to account for small n.
- **Cost validity:** bijective `250+500*10*novelty` rejected; honest API usage + browser count+ms only when LLM available; otherwise cost null with reason api_key_absent. Distill 1000 tok amortized only to SPIDER, instruction 200/f only to INSTR, retrieval 200 tok, verification 50 tok all measured.
- **Validity threats:** single-family ceiling not generalizable to 10-family; file-based synthetic census not production Docker DOM; tool-order/precondition invariants not tested beyond deterministic _matches; path dependence prior not established as SPIDER evidence — all disclosed as do_not_assume.
- **Stale kernel threat:** if grep/sha/diff or unit tests fail, measurement is invalid before B — mitigated by frozen gate 1.
- **Parent handoff supersede threat:** C-FRESHNESS established orthogonality and HS256 fix do not imply param-inherit readiness; conflating lanes would misattribute product readiness. Mitigated by explicit SUPERSEDE disposition and independent kernel/census gates.

---

## 11. Product consequences

**If SURVIVES (binding) or FULL SURVIVES:** advance C-PARAM-INHERIT from EXPERIMENTAL narrow synthetic (10/10 single-param 5.42% saving EXP-PRODUCT-33528829801, 21/21 harness-only multi-param EXP-PRODUCT-33741671686 NOT kernel, 42+ prior KERNEL-INTEGRATION-FALSIFIED/PARTIAL, last 6 Graph MEASUREMENT_INVALID) to VALIDATED at bounded single-family file-based ceiling (one family path+body+headers, deterministic _matches, zero templates, EXECUTABLE>=0.75 binding>=0.90, false_accept<=0.10 UNKNOWN/ECE calibrated, distinct slots, Jaccard>=0.75). First durable proof corrected distill_parameterized (single-prefix, field-filter, Jaccard distinct slots conf 0.90) in src/spider/kernel.py generalizes A→B. If FULL SURVIVES additionally (LLM success +0.12 vs each baseline incl. INSTR, economics >=25% at f=10, cost ratio <=0.85 vs RAG with bootstrap CIs not crossing 1.0), unblocks C-LLM-INHERIT/C-RESIDUAL-NOVELTY/C-PRODUCT-ECON scale-up to 10-family (60 tasks) and Docker full-DOM hosting; informs productization vs TERX 0-token replay dominance (SPIDER wins where replay misses, h~8% routine ceiling addressed by tool-level compilation per Frontier thesis). Authorizes kernel promotion (promotion_ready true, pending kernel tests). No immediate SHIPPED; requires replication on >=10 families and freshness hardening.

**If FALSIFIED on binding (F1/F2):** C-PARAM-INHERIT remains EXPERIMENTAL at narrow synthetic ceiling; for this single-family setting parameterized transfer falsified despite durable src fix (double-prefix/Jaccard/field-filter insufficient or false_accept/ECE fails). Product must NOT promote kernel fix as VALIDATED; next Graph pulse pivots to orthogonal high-upside per Director portfolio (Intel within-store transfer, Frontier JIT/workflow compilation O(1) cost thesis beyond per-step retrieval, Runtime distributed freshness/shared-store) rather than enlarging to 10-family before binding gate passes — lower information per cost of broad census with same kernel bugs. Captures work-compression limit if h~8% ceiling holds at tool level.

**If MIXED (binds but no LLM margin when LLM available):** investigate Playwright execution or agent prompt, not just induction; binding gate still VALIDATED-narrow but economics falsified.

**If MEASUREMENT_INVALID:** fix durable src integration (single-prefix, field-filter url/body.*/headers.* only, Jaccard ≥0.75 distinct slots) + file-based census via Docker/static export before re-testing economics; LLM absence alone preserves binding information (NOT_APPLICABLE for F3/F4). Negative still high information: definitively isolates whether src kernel fix sufficient for EXECUTABLE/binding before spending LLM budget on 60-task multi-family or relying on transient harness patches that repeat 6 prior MEASUREMENT_INVALID pilots. Therapeutic for stalled Graph lane (IDLE → valid measurement).

---

## 12. Estimated cost & information gain

File-based pilot without LLM: ~0 API, ~5 min wall-clock on GitHub Actions (census load, kernel unit tests 16-19 tests, distill 3-5 A → 1 mechanism, resolve+verify 10-16 B tasks via deterministic _matches, 5000 bootstrap, Wilson CIs). With LLM optional (NOT required for binding gate): $3–$8 for 10–16 B tasks ×5 conditions (50-80) + PCs/NCs; 15–25 min wall-clock with 4-way batching. Storage: per-task CSV ~100 rows, registry JSON, cost_config, census verification log, kernel sha+grep+diff, provenance with commits/run ids/dataset hashes. Deterministic seeds, all hashes logged. Honest cost includes tokens+browser+retrieval+verification at f=10 amortized.

Expected information gain: **HIGH** — first durable valid test of central promise after 42+ failed kernel integrations and 6 transient-provenance MEASUREMENT_INVALID pilots; isolates binding prerequisite that can FALSIFY centralized parameterization before 60-task spend (vs broad >=10 families >=60 tasks that produced 5 MEASUREMENT_INVALID in a row with same kernel bugs, inflated scope, lower information per cost). Either positive (EXECUTABLE>=0.75 Wilson lower>=0.65 binding>=0.90 lower>=0.80 zero templates with durable src fix, deterministic verification, false_accept<=0.10 UNKNOWN [0.00,0.15] ECE<=0.15, plus when LLM available success margin>=0.12 vs each baseline via 5000-bootstrap and honest f=10 saving) or valid negative (no executable/binding on never-observed B where duplication 0.9479 requires genuine parameterization, exact-copy 0.0781) decisively changes promotion decision: (1) whether C-PARAM-INHERIT advances EXPERIMENTAL→VALIDATED-narrow and justifies kernel promotion, (2) whether to scale to 10-family 60-task and unblock C-LLM-INHERIT/C-PRODUCT-ECON vs pivoting to orthogonal high-upside (Frontier JIT/workflow compilation O(1) cost thesis, Intel BrowserGym diverse sampling), (3) whether distinct-slot field-path induction solves double-prefix (user-4) and hallucination (E1) at src integration. Resolves starved-claim bottleneck (0/60 recent Graph valid) with minimal spend (10 vs 60 tasks) independent of distributed HS256 store per Director comparative reasoning. Tests Director's agent priors (path dependence, h~8%, verification economics, tool-order invariants) as falsifiable gates, not assumptions.

---

## 13. Reproducibility

Frozen inputs hashed (request.json, spec.json, prereg.md, pilot_family.json, src/spider/kernel.py patch diff vs base_sha 98b40ef4df6bac37548b4dbbbd823ccceaed35a1, census hash, proxy constants, thresholds) in freeze.json. Seeds deterministic (PYTHONHASHSEED=0, random 42, LLM 42 if used, bootstrap 42). Raw evidence preserved: per-task CSV with tokens/calls/latency/success/bound_action/verification/UNKNOWN/false_accept/ECE bins where LLM available else binding-only CSV; registry JSON with slots/templates; cost_config JSON; census verification log (hash, duplication stats, pool A/B value sets zero-overlap SHA256); provenance.json with commits, run ids, dataset hashes, census verification, kernel sha256+grep hits+git diff vs base_sha. Artifact paths + SHA256 logged. No LLM proxy if LLM unavailable — report null with reason api_key_absent. Stable metric/control identities for downstream transmission. Parent handoff SHA 7e120ac preserved but superseded.

---

## 14. Prereg freeze attestation

This prereg is frozen before any outcome-bearing measurement on held-out B. Any change after seeing B outcomes is exploratory and requires new prereg + untouched evidence. Kernel gate verified before B measurement; census zero-overlap verified before distill. Thresholds (EXECUTABLE 0.75 lower 0.65, binding 0.90 lower 0.80, false_accept 0.10, UNKNOWN [0.00,0.15], ECE 0.15, success margin 0.12, saving 25% at f=10, cost ratio 0.85, Jaccard 0.75, confidence 0.90) are frozen and will not be weakened after seeing outcomes per AGENTS.md failure discipline. 5000-bootstrap (seed 42) and Wilson CIs are primary uncertainty methods; no Gaussian jitter. All agent priors are labeled as priors, not SPIDER evidence. Base sha 98b40ef4df6bac37548b4dbbbd823ccceaed35a1 is immutable per request.json.

