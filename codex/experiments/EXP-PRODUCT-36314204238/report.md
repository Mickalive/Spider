# EXP-PRODUCT-36314204238 — C-PARAM-INHERIT: is parameter binding learned or a string matcher?

- **lane**: product
- **status**: `COMPLETE`
- **outcome**: `INCONCLUSIVE`
- **frozen outcome, applied verbatim** (prereg §9): {'B': 'MEASUREMENT_INVALID', 'R': 'MEASUREMENT_INVALID'}
- **primary frame**: `R` — raw goal, full identifier in the request
- **supplementary frame**: `B` — bare-ordinal goal, identifier absent from the request

## 1. The decision the frozen rule actually made

### Frame B — B = bare-ordinal goal, identifier absent from the request

```
IF any F5-F8 triggered:
   F5 substrate contract violation = False
   F6 degenerate discriminative power = True
   F7 cost model integrity failure    = False
   F8 commit hash mismatch           = NOT_EVALUABLE
   outcome = INCONCLUSIVE (F5) or MEASUREMENT_INVALID (F6-F8)  -> taken: F6-F8: F6
ELIF all F1-F4 false: outcome = SUPPORTS   -> NOT REACHED, rule short-circuits above
ELIF any F1-F4 true: outcome = FALSIFIES  -> NOT REACHED; for the record F1-F4 fired: none
```

Frozen outcome: **MEASUREMENT_INVALID**, decided at `F6-F8`.

### Frame R — R = raw goal, full identifier in the request

```
IF any F5-F8 triggered:
   F5 substrate contract violation = False
   F6 degenerate discriminative power = True
   F7 cost model integrity failure    = False
   F8 commit hash mismatch           = NOT_EVALUABLE
   outcome = INCONCLUSIVE (F5) or MEASUREMENT_INVALID (F6-F8)  -> taken: F6-F8: F6
ELIF all F1-F4 false: outcome = SUPPORTS   -> NOT REACHED, rule short-circuits above
ELIF any F1-F4 true: outcome = FALSIFIES  -> NOT REACHED; for the record F1-F4 fired: ['F1']
```

Frozen outcome: **MEASUREMENT_INVALID**, decided at `F6-F8`.

The rule tests F5–F8 before F1–F4. F6 asks whether *any* arm has a success interval of exactly [1.0, 1.0]. With 100 in-support tasks per cell drawn from one synthetic identifier distribution, a binder that is correct on every one of them has no bootstrap variability, so its interval collapses to [1.0, 1.0] — as do A7/A8/A9, which are correct by construction because they never bind at all. F6 is therefore satisfied by perfection and by non-mechanised baselines alike, and it short-circuits the primary comparison before it is read.

**This is a defect in the frozen decision rule, not a defect in the measurement.** 10 arm series x 5 cost multipliers x 2 goal frames = 100 cells and 10000 task measurements ran, every substrate contract check passed, and every request/response pair was preserved. The F1–F4 panel is therefore reported in full below so that the masking is auditable rather than convenient.

## 2. What the F1–F4 panel says (computed, not reached)

| Falsifier | Frame R | Frame B | What it measured |
|---|---|---|---|
| F1 — Bind accuracy failure | false | **TRIGGERED** | Bind accuracy failure |
| F2 — Semantic guard failure | false | false | Semantic guard failure |
| F3 — Execution gap | false | false | Execution gap |
| F4 — Transfer pattern violation | false | false | Transfer pattern violation |
| F5 — Substrate contract violation | false | false | Substrate contract violation |
| F6 — Degenerate discriminative power | **TRIGGERED** | **TRIGGERED** | Degenerate discriminative power |
| F7 — Cost model integrity failure | false | false | Cost model integrity failure |
| F8 — Commit hash mismatch | not evaluable | not evaluable | Commit hash mismatch |

**F1 detail, frame B**: A1 CI95 lower = 1.0; max null CI95 upper = 0.0 (margin 1.0). A4's own upper bounds: {'A4:longest_first': 0.0, 'A4:shortest_first': 0.0}.
**F1 detail, frame R**: A1 CI95 lower = 1.0; max null CI95 upper = 1.0 (margin 0.0). A4's own upper bounds: {'A4:longest_first': 0.0, 'A4:shortest_first': 1.0}.

## 3. Per-arm results

### Frame B — B = bare-ordinal goal, identifier absent from the request

| Arm | Tie order | Series | In-support bind accuracy (CI95) | Semantic false-accept | Abstain | Selective acc. | UNKNOWN precision | Req/task @ mult 1 |
|---|---|---|---|---|---|---|---|---|
| A1 | - | variability_learned_multi_collection | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0.5 | 1.0 | 1.0 | 0.5 |
| A2 | - | variability_learned_single_collection | 0.340 [0.340, 0.340] | 0.000 [0.000, 0.000] | 0.83 | 1.0 | 0.60241 | 0.17 |
| A3 | - | declared_vocabulary_incumbent | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.0 | 1.0 | None | 1.0 |
| A4 | longest_first | null_lexical_overlap | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0.0 | 0.0 | None | 1.0 |
| A4 | shortest_first | null_lexical_overlap | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0.0 | 0.0 | None | 1.0 |
| A5 | - | null_positional_regex | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 1.0 | None | 0.5 | 0.0 |
| A6 | - | null_most_frequent_value | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0.0 | 0.0 | None | 1.0 |
| A7 | - | baseline_cold_re_derivation | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.0 | 1.0 | None | 3.0 |
| A8 | - | baseline_within_episode_scratchpad | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.0 | 1.0 | None | 1.08 |
| A9 | - | baseline_retrieval_k5 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.0 | 1.0 | None | 1.0 |

### Frame R — R = raw goal, full identifier in the request

| Arm | Tie order | Series | In-support bind accuracy (CI95) | Semantic false-accept | Abstain | Selective acc. | UNKNOWN precision | Req/task @ mult 1 |
|---|---|---|---|---|---|---|---|---|
| A1 | - | variability_learned_multi_collection | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0.5 | 1.0 | 1.0 | 0.5 |
| A2 | - | variability_learned_single_collection | 0.340 [0.340, 0.340] | 0.000 [0.000, 0.000] | 0.83 | 1.0 | 0.60241 | 0.17 |
| A3 | - | declared_vocabulary_incumbent | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.0 | 1.0 | None | 1.0 |
| A4 | longest_first | null_lexical_overlap | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0.0 | 0.0 | None | 1.0 |
| A4 | shortest_first | null_lexical_overlap | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.0 | 1.0 | None | 1.0 |
| A5 | - | null_positional_regex | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 1.0 | None | 0.5 | 0.0 |
| A6 | - | null_most_frequent_value | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0.0 | 0.0 | None | 1.0 |
| A7 | - | baseline_cold_re_derivation | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.0 | 1.0 | None | 3.0 |
| A8 | - | baseline_within_episode_scratchpad | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.0 | 1.0 | None | 1.08 |
| A9 | - | baseline_retrieval_k5 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.0 | 1.0 | None | 1.0 |

## 4. The two frames answer different questions

**Frame B separates the mechanisms. Frame R cannot.**

- Frame B: lexical-overlap null in-support bind accuracy is 0.0 (longest-first) versus 0.0 (shortest-first); variability binder is 1.0.
- Frame R: lexical-overlap null in-support bind accuracy is 0.0 (longest-first) versus 1.0 (shortest-first); variability binder is 1.0.

On frame R the goal *is* `verb record <full-id> in <collection> catalog`. A matcher that copies a token out of the request cannot fail, so the frame is outside the null's competence and its score there is not evidence about the null. On frame B the goal is `verb record number <ordinal>`, which contains none of the answer, and the null fails under both tie orders. This is why the request declared B supplementary: it is the frame that actually discriminates, and the primary frame is the one that mostly cannot.

## 5. Mechanism: declared vocabulary versus inferred variability

**A1 multi-collection** — `{"method": "DELETE", "path": "/${s0}/${s1}"}`

- induction basis: `observed_variability`, 150 observations, 150 conforming
- inferred slots: `['s0', 's1']`; declared identity slots: `[]`; declared identity fields: `[]`
- collection slot support: `{"cardinality": 3, "kind": "closed_set", "n_observations": 150, "values": ["items", "orders", "products"]}`
- identifier slot support: `{"kind": "shape", "n_distinct": 150, "n_observations": 150, "prefixes": ["item", "order", "product"], "shape": "[a-z]+\\-[0-9]+"}`
- id_prefix_by_head: `{"items": "item", "orders": "order", "products": "product"}`
- pinned segments: `{}`
- confidence 1.0 (leave-one-out: 60/60 under leave_one_out_random_42_n60); the incumbent's own support-overlap formula would give 0.6667

**A2 items-only** — `{"method": "DELETE", "path": "/items/${s1}"}`

- induction basis: `observed_variability`, 50 observations, 50 conforming
- inferred slots: `['s1']`; declared identity slots: `[]`; declared identity fields: `[]`
- collection slot support: `null`
- identifier slot support: `{"kind": "shape", "n_distinct": 50, "n_observations": 50, "prefixes": ["item"], "shape": "[a-z]+\\-[0-9]+"}`
- id_prefix_by_head: `{"items": "item"}`
- pinned segments: `{"0": "items"}`
- confidence 1.0 (leave-one-out: 50/50 under leave_one_out_random_42_n50); the incumbent's own support-overlap formula would give 1.0

**A3 declared vocabulary** — `{"method": "DELETE", "path": "/${collection}/${id}"}`

- induction basis: `None`, None observations, None conforming
- inferred slots: `['id']`; declared identity slots: `['collection']`; declared identity fields: `['collection', 'resource']`
- collection slot support: `not inferred (declared slots)`
- identifier slot support: `not inferred (declared slots)`
- id_prefix_by_head: `null`
- pinned segments: `null`
- confidence 1.0 (leave-one-out: n/a, the incumbent has no held-out replay); the incumbent's own support-overlap formula would give None

The A1 mechanism contains no collection vocabulary in code. The closed set over `{items, orders, products}` and the head-to-prefix map are *measured* from 150 training observations and are what let it bind `products` at test time and abstain on `widgets`, which was never observed. The A2 mechanism is the same estimator on items alone, so its closed set is `{items}` and it correctly refuses `products`. The A3 mechanism carries `DEFAULT_IDENTITY_FIELDS`-style declared slots and transfers to `products` without ever having observed it — which is exactly the declared-vocabulary behaviour F4 is designed to catch, and exactly the behaviour that produces a 1.0 false-accept rate on well-formed out-of-support identifiers.

## 6. Economics

Break-even is the smallest number of reused tasks at which the arm is strictly cheaper than the measured comparator cell, solved in exact integer request counts. `never` means no number of reuses makes it cheaper. Note that the cost multiplier manipulates *latency*, not request count, so an inheriting arm's request totals are identical at multiplier 1 and 20; only A7 and A8, which genuinely re-derive, scale with it. The measured per-task rate is below 1.0 for A1, A2 and A5 because abstaining costs nothing.

| Frame | Arm | Induction | Req/task @1 | Req/task @20 | Total @1 | Total @20 | vs scratchpad @1 | vs K5 @1 | break-even vs scratchpad | break-even vs K5 |
|---|---|---|---|---|---|---|---|---|---|---|
| B | A1 | 1350 | 0.5 | 0.5 | 1400 | 1400 | 12.962963 | 14.0 | 2328 | 2701 |
| B | A2 | 450 | 0.17 | 0.17 | 467 | 467 | 4.324074 | 4.67 | 495 | 543 |
| B | A3 | 450 | 1.0 | 1.0 | 550 | 550 | 5.092593 | 5.5 | 5626 | never |
| B | A4:longest_first | 1350 | 1.0 | 1.0 | 1450 | 1450 | 13.425926 | 14.5 | 16876 | never |
| B | A4:shortest_first | 1350 | 1.0 | 1.0 | 1450 | 1450 | 13.425926 | 14.5 | 16876 | never |
| B | A5 | 1350 | 0.0 | 0.0 | 1350 | 1350 | 12.5 | 13.5 | 1251 | 1351 |
| B | A6 | 1350 | 1.0 | 1.0 | 1450 | 1450 | 13.425926 | 14.5 | 16876 | never |
| B | A7 | 0 | 3.0 | 60.0 | 300 | 6000 | 2.777778 | 3.0 | never | never |
| B | A8 | 0 | 1.08 | 3.36 | 108 | 336 | 1.0 | 1.08 | never | never |
| B | A9 | 0 | 1.0 | 1.0 | 100 | 100 | 0.925926 | 1.0 | 1 | never |
| R | A1 | 1350 | 0.5 | 0.5 | 1400 | 1400 | 12.962963 | 14.0 | 2328 | 2701 |
| R | A2 | 450 | 0.17 | 0.17 | 467 | 467 | 4.324074 | 4.67 | 495 | 543 |
| R | A3 | 450 | 1.0 | 1.0 | 550 | 550 | 5.092593 | 5.5 | 5626 | never |
| R | A4:longest_first | 1350 | 1.0 | 1.0 | 1450 | 1450 | 13.425926 | 14.5 | 16876 | never |
| R | A4:shortest_first | 1350 | 1.0 | 1.0 | 1450 | 1450 | 13.425926 | 14.5 | 16876 | never |
| R | A5 | 1350 | 0.0 | 0.0 | 1350 | 1350 | 12.5 | 13.5 | 1251 | 1351 |
| R | A6 | 1350 | 1.0 | 1.0 | 1450 | 1450 | 13.425926 | 14.5 | 16876 | never |
| R | A7 | 0 | 3.0 | 60.0 | 300 | 6000 | 2.777778 | 3.0 | never | never |
| R | A8 | 0 | 1.08 | 3.36 | 108 | 336 | 1.0 | 1.08 | never | never |
| R | A9 | 0 | 1.0 | 1.0 | 100 | 100 | 0.925926 | 1.0 | 1 | never |

The incumbent A3 spends exactly one request per task, the same rate as the zero-induction retrieval baseline, so its 450-request induction is never recovered against A9: it is dominated for every episode length. A1 recovers its 1350-request induction only after about 2,300 reused tasks against within-episode priming, and about 2,700 against retrieval, because abstaining on half its tasks makes its per-task rate half that of either comparator. Cost is also the only axis on which the baselines look acceptable: their semantic false-accept rate is 1.0, against 0.0 for A1, because every one of them executes a well-formed out-of-support identifier they cannot justify. So on this cost basis cross-episode induction is not merely slower to amortise, it is the only family here that refuses requests it cannot justify. None of this speaks to cross-site economics, where the alternative is re-paying discovery per site rather than within one episode.

## 7. What this run does and does not establish

**Establishes (as measurement, under the frozen F1–F4 definitions):**

1. A variability binder inferred purely from observed path-segment distributions binds held-out identifiers of seen collections at the ceiling in both frames.
2. It refuses well-formed identifiers of an unseen collection, where the declared-vocabulary incumbent executes them. This is the cleanest measured difference in the packet and it is not cost-dependent.
3. Its transfer profile is the one the frozen rule calls variability success: items-only training does not transfer, multi-collection training does.
4. Both structural nulls (positional-regex, most-frequent-value) and, on frame B, the lexical-overlap null, fail to reproduce the treatment.
5. Cross-episode induction is economically dominated within this cost basis.

**Does not establish:**

1. Nothing about the claim status of `C-PARAM-INHERIT` under this experiment's own frozen rule, which returns MEASUREMENT_INVALID. Promotion requires an audit and a Director verdict; the producer does not self-promote.
2. Nothing about multi-template routes, real Web latency, cross-site transfer, or any LLM in the loop. The substrate is a single-template deterministic stdlib server.
3. Nothing about whether A4's frame-R score reflects the null's genuine weakness or the frame being outside its competence.

**The single most useful next experiment** is not another arm. It is a repaired decision rule plus a harder identifier distribution: fix or remove the A4 tie rule, order F1–F4 before the degeneracy guard, widen the in-support identifier distribution so intervals are informative, and then re-run. The mechanism result is already clear enough that repeating it without those repairs would not add information.

## 8. Evidence index

- `research/experiments/EXP-PRODUCT-36314204238/raw_evidence/observations.jsonl` — raw, sha256 `85aae781d56b9580…`
- `research/experiments/EXP-PRODUCT-36314204238/raw_evidence/bind_results.jsonl` — raw, sha256 `7fe5e2dc55140379…`
- `research/experiments/EXP-PRODUCT-36314204238/raw_evidence/exec_results.jsonl` — raw, sha256 `89c045b713da8629…`
- `research/experiments/EXP-PRODUCT-36314204238/raw_evidence/induction_observations.jsonl` — raw, sha256 `d63ae5b6e4bbdd39…`
- `research/experiments/EXP-PRODUCT-36314204238/raw_evidence/probe_results.jsonl` — raw, sha256 `e167cde1fba1ef98…`
- `research/experiments/EXP-PRODUCT-36314204238/raw_evidence/substrate_probe.json` — raw, sha256 `920f0d75dcef87e2…`
- `research/experiments/EXP-PRODUCT-36314204238/raw_evidence/mechanisms_raw.json` — raw, sha256 `09cba80e006d258c…`
- `research/experiments/EXP-PRODUCT-36314204238/raw_evidence/run_config.json` — raw, sha256 `f4f6dfcac2177568…`
- `research/experiments/EXP-PRODUCT-36314204238/raw_evidence/derived.json` — derived, sha256 `3e51740c499c93da…`
- `research/experiments/EXP-PRODUCT-36314204238/raw_evidence/mechanisms.json` — derived, sha256 `2b35dc420489c0fc…`
- `research/experiments/EXP-PRODUCT-36314204238/substrate.py` — code, sha256 `6ad7e1ed8f6f2143…`
- `research/experiments/EXP-PRODUCT-36314204238/run_experiment.py` — code, sha256 `18132272758e9489…`
- `research/experiments/EXP-PRODUCT-36314204238/build_result.py` — code, sha256 `82de7799fec1954a…`
- `research/experiments/EXP-PRODUCT-36314204238/request.json` — fixture, sha256 `9131a601245863ca…`
- `research/experiments/EXP-PRODUCT-36314204238/spec.json` — fixture, sha256 `011e7900b2334aeb…`
- `research/experiments/EXP-PRODUCT-36314204238/prereg.md` — fixture, sha256 `5de0826934a7c531…`
- `research/experiments/EXP-PRODUCT-36314204238/freeze.json` — fixture, sha256 `eec5bf1850ae51c5…`

Full falsifier panel, per-cell metrics and bootstrap detail: `raw_evidence/derived.json`.

