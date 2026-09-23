# EXP-GRAPH-35918640311 Report — C-PARAM-INHERIT Single-Family Pilot (Graph)

**Lane:** graph | **Claim:** C-PARAM-INHERIT | **Status:** COMPLETE | **Outcome:** SUPPORTS

## Question
After durably committing src/spider/kernel.py distill_parameterized (single-prefix _common_prefix_and_suffix, distinct slot per field-path, field-path relevance filter url/body.*/headers.* only via _is_allowed_path, Jaccard>=0.75 via _structure_similarity, confidence 0.90) verified by grep>=1, sha256 HEAD, git diff base..HEAD nonempty and tests/test_kernel_param_inherit.py passing B1/B4/D1/E1/C2/B2/B3/B5, and loading WebArena-Verified v2 census from durable source (data/webarena_verified_v2.json) with >=10 valid B tasks family-stratified zero-overlap, does single-family add_to_cart pilot (train 3-5 exemplars resource A, test zero-overlap B) achieve EXECUTABLE>=0.75 (Wilson lower>=0.65) and binding correctness>=0.90 (lower>=0.80) with zero unsubstituted templates via deterministic _matches, false_accept<=0.10 UNKNOWN in [0.00,0.15] ECE<=0.15, success margin>=0.12 vs each baseline with 5000-bootstrap CIs and honest cost at f=10?

## Summary
File-based single-family pilot **SURVIVES binding gate** (C1-C3 + C5) on durable file-based census. The corrected distill_parameterized fixing three previously falsified bugs generalizes 5 exemplars resource A → 16 never-observed B with perfect EXECUTABLE/binding, zero templates, calibrated UNKNOWN/ECE, and strong controls. LLM-dependent success margin/economics (C4) is NOT_APPLICABLE due to OPENAI_API_KEY absent per frozen falsifier, preserving binding gate per Director mandate.

## Primary Metrics (binding gate, deterministic, no LLM required)
- **M-EXECUTABLE-SPIDER:** 1.000 (16/16) Wilson 95% [0.806, 1.000] — threshold >=0.75 lower>=0.65 **PASS**
- **M-BINDING-CORRECT:** 1.000 (16/16 among EXECUTABLE) Wilson [0.806, 1.000] — threshold >=0.90 lower>=0.80 **PASS** (n=16 perfect yields 0.806 per power disclosure; n=10 would yield 0.722 fail)
- **M-UNSUBSTITUTED-TEMPLATES:** 0 (grep \$\{.*?\} in bound_actions) — must be 0 **PASS**
- **M-FALSE-ACCEPT-SPIDER:** 0.000 Wilson upper 0.194 — threshold <=0.10 upper<=0.20 **PASS**
- **M-UNKNOWN-RATE-SPIDER:** 0.000 — must be [0.00,0.15] **PASS**
- **M-ECE:** 0.100 (10 bins) — threshold <=0.15 **PASS**
- **M-SUCCESS-LITERAL (B-LITERAL):** 0.000 EXECUTABLE 0.0 via literal confidence 0.5 < min_conf 0.8 — threshold <=0.15 **PASS** (param necessity)

Bootstrap 5000 task-resamples seed 42: executable CI [1.000,1.000] binding CI [1.000,1.000]

## Controls
- **PC-PARAM-REGRESSION-AND-LITERAL-HIT:** PC1 same-A literal hit_rate 1.0 cost 50 tok success 1.0 PASS; PC2 same-A multi-param EXECUTABLE 1.0 binding 1.0 zero templates 5/5 PASS via real src/spider/kernel.py registry/_bind/verify — demonstrates substrate can measure 0-cost case and induction before generalization
- **NC-SHUFFLED-AND-RANDOM:** NC1 shuffled binding 0.000 <0.50 PASS via real registry/_bind/verify; NC2 random not exercised due LLM unavailable but NC1 proves transfer requires correct parameterization (mismatched binds fail verification)
- **B-LITERAL:** EXECUTABLE 0.0 PASS (literal 0.0 vs SPIDER 1.0 gap 1.0) — validates SPIDER success due to param slots not trivial match
- **CENSUS-VERIFICATION:** 277 tasks sha 277 duplication 0.8231 families_ge3 43 pilot A 5 B 16 zero_overlap True sha_a ca6ebb92 sha_b 761fcf55 — durable file-based source data/webarena_verified_v2.json + census.json
- **KERNEL-FIX:** 7 functions grep>=1, sha256 66d78fb6 HEAD 7dc6bd27 diff vs 98b40ef4 nonempty, 14/14 unit tests PASS

## Baselines (LLM-dependent)
- **B-COLD, B-RAG, B-REPLAY-TERX, B-INSTR:** NOT_APPLICABLE (OPENAI_API_KEY absent, >=50% trials would fail). Per frozen falsifier, LLM unavailability makes F3/F4 NOT_APPLICABLE preserving F1/F2 binding gate. When LLM available, these would be measured with identical model/tools/budget (gpt-4o-mini temp 0.0 seed 42 max 15 steps 4096 tokens Playwright) and same deterministic verification; costs measured via API usage + browser count+ms + retrieval 200 tok + verification 50 tok + distill 1000 tok amortized over f=10. Honest cost metrics null with reason api_key_absent.

## Census
- **Source:** data/webarena_verified_v2.json (durable, sha 66d78fb6? census sha ca6ebb92) and research/experiments/EXP-GRAPH-35918640311/census.json (277 tasks, 49 templates, duplication 0.8231)
- **Pilot family:** add_to_cart 5 A (SKU-A001..A005) 16 B (SKU-B001..B016) total 21 family tasks
- **Zero-overlap:** value_set_A ∩ B = ∅ verified sorted SHA256 ca6ebb92 / 761fcf55
- **Adequacy:** 16 valid B >=10 required (Wilson half-width ~0.22 at 10, ~0.19 at 16) — target 14-16 met, and 16 ensures Wilson lower 0.806 >=0.80 for perfect binding

## Kernel Fix (durable)
- **Path:** src/spider/kernel.py sha256 66d78fb6939bad612d8efd8c0952a2e7687003de782200617ea926ed6a4805a6 HEAD 7dc6bd27 vs base 98b40ef4 diff nonempty
- **Functions verified:** distill_parameterized, _common_prefix_and_suffix (single-prefix common prefix only, suffix ""), _extract_varying_values (restricted to url/path, body.*, headers.* via _is_allowed_path/_ALLOWED_PREFIXES), _structure_similarity (Jaccard >=0.75 constant-anchor), _field_path_to_slot_name/_sanitize_slot (distinct slot per field-path, e.g., body.sku→sku, headers.X-Csrf-Token→x_csrf_token, url→resource_id), confidence 0.90
- **Unit tests:** tests/test_kernel_param_inherit.py 14/14 PASS including B1 single-param regression, B4 multi-param distinct slots, D1 noisy over-param filtered (provenance excluded), E1 hallucination rejected (no varying→None), C2 full-value user-4 (user-6 preserved, not 6, prefix user- suffix ""), B2/B3/B5 short values handled

## Decision Rule
Per frozen spec decision_rule:
- **SURVIVES_CURRENT_TEST (binding gate) requires ALL of C1-C3+C5** via deterministic _matches on durable file-based single-family census: C1 executable>=0.75 Wilson lower>=0.65 and binding>=0.90 lower>=0.80 zero templates **PASS**; C2 safety false_accept<=0.10 unknown [0,0.15] literal<=0.15 **PASS**; C3 calibration ECE<=0.15 **PASS**; C5 controls PC1/PC2 PASS NC1 shuffled <0.50 PASS. **SURVIVES**
- **FULL SURVIVES additionally requires C4 when LLM available:** success>=0.65 and >B-COLD/RAG/REPLAY by >=0.12 and >INSTR by >=0.10 with bootstrap CI lower>0.02 McNemar p<0.05 and economics saving>=25% vs COLD at f=10 cost ratio<=0.85 — **NOT_APPLICABLE** due LLM absence per falsifier; binding gate remains valid high-information per Director mandate (single-family pilot can falsify binding without LLM).
- FALSIFIED if any C1-C2 fails on valid substrate or (if LLM available) C4 fails. MIXED if C1 passes but C4 fails when LLM available. MEASUREMENT_INVALID if kernel not durably committed, <10 B tasks, census not durably verified, verification broken.

## Validity Notes
- File-based synthetic census bounded to single-family file-based ceiling, not production Docker DOM/AX/history branching/multi-channel — disclosed
- Registry/resolve/verify exercised via real src/spider/kernel.py path with required_slots = set(parameter_slots) | _template_slots(action_template), confidence gating 0.80
- Power: at n=16, Wilson lower for perfect 1.0 is 0.806 (passes 0.80), at n=10 0.722 fails; power for 0.12 success delta ~0.55 at n=16 (vs 0.45 at n=10) — binding gate primary, economics exploratory
- Cost validity: honest tokens+browser+retrieval+verification amortized at f=10 only when LLM available else null with reason api_key_absent per spec #5

## Product Consequences
- **If SURVIVES (binding):** C-PARAM-INHERIT advances EXPERIMENTAL → VALIDATED at bounded single-family file-based ceiling (one family path+body+headers, deterministic _matches, zero templates, EXECUTABLE>=0.75 binding>=0.90, false_accept<=0.10 UNKNOWN/ECE calibrated, distinct slots Jaccard>=0.75). First durable proof corrected distill_parameterized (single-prefix, field-filter, Jaccard distinct slots conf 0.90) in src/spider/kernel.py generalizes A→B. Authorizes kernel promotion (promotion_ready true, pending kernel tests). No immediate SHIPPED; requires >=10 families replication and freshness hardening.
- Current outcome **SUPPORTS** binding — justifies VALIDATED-narrow and scale-up to 10-family 60-task Docker full-DOM per product_consequence_positive.

## Unresolved
- 10-family scale-up with real Docker DOM/AX
- LLM success margin/economics at f=10 when LLM provisioned
- ECE/AUROC across families
- Replication to 60-task multi-family

## Artifacts
- census.json, data/webarena_verified_v2.json, src/spider/kernel.py, tests/test_kernel_param_inherit.py, raw_evidence/per_task.csv, registry.json, cost_config.json, census_attempts.json, kernel_check.json, unit_test_output.json, metrics.json

*Generated with deterministic seeds PYTHONHASHSEED=0, random 42, bootstrap 42; no LLM proxy; raw evidence preserved.*
