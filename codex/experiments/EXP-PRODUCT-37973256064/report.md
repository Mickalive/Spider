# Report: EXP-PRODUCT-37973256064

**Lane**: product  
**Claim**: C-PARAM-INHERIT ("Mechanisms parameterize to unseen identifiers")  
**Status**: COMPLETE  
**Outcome**: FALSIFIES  
**Schema version**: 1

## Executive summary

Executed the frozen credential-free real localhost stdlib-HTTP substrate experiment. The treatment arm (T-SPIDER-PARAM) achieved **success_rate 0.80** on held-out identifiers (12/15 tasks). Cold re-derivation (B-COLD-RE-DERIVE) and retrieval-shaped comparator (B-RETRIEVAL-SHAPED) both achieved **1.00**. Known negatives, null control on unseen type, accounting honesty, causal attribution (literal 0.0, positive control 1.0), and substrate validity all passed. The PRIMARY decision clause failed because treatment advantage vs cold/retrieval was **~ -0.20** (not > 0.15). Per prereg §7, this maps to **FALSIFIES** with **status=COMPLETE** (valid scientific negative).

## Substrate and implementation (frozen)

- Real `http.server.HTTPServer` on ephemeral localhost; responses include `Content-Type: application/json` and `X-Request-Id`. Three resource types: items/users/orders, 10 identifiers each. Training A = 001..005, held-out B = 006..010; unseen type products for null control.
- `src/spider/kernel.py` contains audited repair including `distill_parameterized`; mechanisms induced with `confidence 0.90` and `parameter_slots=[type]` (items->item, users->user, orders->order), templates e.g. `http://.../api/items/${item}`. 
- `src/spider/__init__.py` exports `TrajectoryCounters`. Audited `tests/test_kernel.py` (9 tests) still PASS under `python3 -m unittest discover -s tests -v` (run before freeze; not re-run here to avoid changing state). 
- Harness: `harness/substrate.py` (server/client), `harness/run_experiment.py` (arms, accounting, raw/derived output). Accounting uses a `LoggingCounters` sink writing per-increment events with timestamps; model_calls/model_tokens remain 0 for all arms.

## Raw/derived artifacts (hash-verified)

All artifact paths and sha256s match those recorded in `artifacts[]`. Key files: `raw_evidence/training_observations.jsonl` (15 observations), `raw_evidence/induced_mechanisms.json` (3 mechanisms with inferred parameter support regexes), `raw_evidence/task_trajectories.jsonl` (all test tasks), `raw_evidence/accounting_counters.jsonl` (real increment events), `raw_evidence/known_negatives.jsonl`, `raw_evidence/null_control_unseen_type.jsonl`, `raw_evidence/server_log.jsonl` (~72 HTTP requests), `derived/arm_metrics.json`, `derived/decision_rule_eval.json`.

## Mechanism inference (observed)

Induced mechanisms:
- items: `mechanism_id mech-48a706c9600e8647`, slot `item`, template `/api/items/${item}`, supports `{"item": "^item\\-00[0-9]{1}$"}` (i.e. `item-00d` with d in 0-9)
- users: similar `^user\\-00[0-9]{1}$`
- orders: similar `^order\\-00[0-9]{1}$`

This matches the training set (001..005). Held-out B includes `010` for each type (two digits: '0','1','0'); the inferred support regex requires the second character of the suffix to be '0' in `00[0-9]`, so `010` falls outside inferred support. Consequently treatment arm rejects `item-010`, `user-010`, `order-010` at resolve time (`EXPLORE | parameter ... outside inferred support`) producing 3 failures out of 15. Cold and retrieval construct/copy correct URLs directly and succeed (1.0).

## Arm performance

| Arm | n_tasks | success | success_rate | http_requests | retrieval_calls | verification_calls | model_calls |
|---|--------|---------|--------------|---------------|------------------|--------------------|-------------|
| T-SPIDER-PARAM | 15 | 12 | 0.800 | 12 | 15 | 12 | 0 |
| B-COLD-RE-DERIVE | 15 | 15 | 1.000 | 15 | 0 | 15 | 0 |
| B-RETRIEVAL-SHAPED | 15 | 15 | 1.000 | 15 | 45 | 15 | 0 |
| PC-EXACT-REPLAY | 15 | 15 | 1.000 | 15 | 15 | 15 | 0 |
| B-LITERAL-KERNEL | 15 | 0 | 0.000 | 0 | 0 | 0 | 0 |

## Controls and decision rule

- **PRIMARY**: treatment_rate 0.80 >= 0.80 is TRUE, but advantages vs cold (-0.20) and vs retrieval (-0.20) are NOT > 0.15 → **fail**.
- **KNOWN-NEGATIVE**: refusal_rate 1.00, reason_correctness 1.00, all bound_action null → **PASS**. Covers out-of-support, missing_parameter, wrong_intent (wrong_intent resolves as UNKNOWN with "no applicable validated mechanism").
- **ACCOUNTING_HONESTY**: model_calls_total 0, model_tokens_total 0, no injected events → **PASS**. Counter events written per increment (real increments) with timestamps; per-task totals in trajectories match aggregates.
- **CAUSAL_ATTRIBUTION**: literal kernel 0.0 < 0.20, PC-EXACT-REPLAY 1.0 → **PASS**. Treatment's failure mode is conservative support inference, not lack of causal mechanism path.
- **SUBSTRATE_VALIDITY**: real localhost HTTP, 3 types × 10 ids each, not SYNTH-INDUCTION-BANK-v1 → **PASS**.
- **OVERALL**: **FALSIFIES** (PRIMARY fails; others pass). status=COMPLETE.

## Interpretation (bounded)

The experiment does **not** demonstrate the parameterized mechanism's advantage over cold/retrieval on this held-out set because `distill_parameterized` inferred a narrow support regex from 5 examples and rejected `-010`. This is a support-generalization/induction detail of the current implementation, not a failure of substrate, accounting, or causal attribution. Cold and retrieval are strong baselines here (deterministic, correct URL construction trivial) and legitimately achieve 1.0.

The result is a **valid scientific negative** for the specific frozen design's primary claim. It does not reject the broader notion of parameterization; it bounds the implementation (support inference/generalization) as the limiting factor on this held-out set. The experiment succeeded in establishing liveness/separation controls, real-substrate execution, and honest accounting; the primary margin was not met due to conservative support bounds.

## Unresolved

- **U-SUPPORT-GENERALIZATION**: Should `distill_parameterized` generalize support (e.g. from 001..005 to 001..010 as a contiguous sequence) or require explicit evidence? Current behavior produces a conservative regex. This is a kernel design question that could be tested by re-running with widened support inference or with training including boundary examples, but such changes would modify the frozen mechanism-induction logic; under frozen EXECUTE rules we do not alter design after seeing outcomes.

## Reproducibility

- Git HEAD: 86722252623bc674c4fb37da8150b86928684950 (frozen execution base)
- Frozen inputs: request.json sha256 c2f57848..., spec.json sha256 1733f30b..., prereg.md sha256 0938f9c3... (verified)
- Kernel blob: b15ed848 (sha256 718efa6a...) in `src/spider/kernel.py`; tests `src/spider/__init__.py` sha256 de7a453a, `tests/test_kernel.py` sha256 89a1b9b9
- Run command: `PYTHONPATH=src timeout 300 python3 research/experiments/EXP-PRODUCT-37973256064/harness/run_experiment.py` (completed exit 0)

## Next steps (advisory, not executed)

This is a bounded negative on the frozen design. If the director wants to test parameterized advantage on this substrate, a minimal redesign could: (1) include `-010` in training or adjust support inference to be less conservative for numeric sequences, or (2) redefine held-out set to remain within inferred support. Any such change would require a new frozen design (new request/spec/prereg/freeze) under SPIDER Research 2.0 discipline; it must not be retrofitted into this experiment.
