# EXP-FRONTIER-36287182510 — within-episode binding propagation vs. cross-episode binding-keyed compilation

## 1. Status, and what it means

- `status`: **COMPLETE** (measurement validity)
- `outcome`: **MIXED** (spec.json frozen outcome vocabulary)
- frozen decision label (spec.json 6 / prereg.md 3): **SCRATCHPAD_CORRECT_BUT_COSTLY**
- falsifier clauses: clause 1 fired = **False**, clause 2 fired = **False** (leg a True, leg b False), clause 3 fired = **False** (leg a True, leg b False)
- no-go conditions fired: **none**

Read this as: the two preregistered memory mechanisms are *separated* on this substrate, and the frozen
decision rule is reported exactly as measured. The clause table below is the whole scientific result;
everything after section 3 is its audit trail.

## 2. The decision, in the frozen vocabulary

| clause | arm | leg (a) correctness >= 0.9833 | leg (b) cost <= 38.6 | fires |
|---|---|---|---|---|
| clause_2 | WITHIN_EPISODE_SCRATCHPAD | 1.0000 (PASS) | 48.00 (FAIL) | **False** |
| clause_3 | CROSS_EPISODE_COMPILED_BINDING | 1.0000 (PASS) | 48.20 (FAIL) | **False** |

`SCRATCHPAD_CORRECT_BUT_COSTLY` -> `MIXED`. The clause-1 precondition (sigma_2 CI95 upper < 0.01 at all five
novelty rates) was **False**, so the experiment is a valid measurement of the clause 2/3
tradeoff and not a statement about the residual.

## 3. Frozen design vs. what was measured (audit readers: start here)

Every plan below is fixed in `request.json` / `spec.json` / `prereg.md` before execution and hashed in
`freeze.json`; this run recomputed all three hashes and they match.

- **Inheritance**: this run exists to answer the parent auditor's 8 `required_fixes`; section 10.1 gives
  the per-fix disposition. The parent packet closed at `audit_status=REVISE`.
- **Primary endpoint** (prereg.md 10.1): span-level *action* correctness — the emitted `(method, path, body)`
  against the declared plan action bound at execution time, from a **shared ground truth** recorded
  independently of any arm. The parent used end-of-episode goal-state success, which cannot discriminate
  these arms; section 9 measures exactly how blind it is.
- **Arms** (6, all on the identical 24-step plan family, 50 episodes x 5 novelty rates = 6000 span occurrences):
  `B-NO-MEMORY-DETERMINISTIC` (inherited reference, unchanged), `B-NO-MEMORY-CONDITIONED-WIDE` and `B-NO-MEMORY-CONDITIONED-NARROW` (inherited
  conditioned baselines), `B-COLD-EXPLORATION` (inherited cost anchor), `WITHIN_EPISODE_SCRATCHPAD` (within-episode scratchpad),
  `CROSS_EPISODE_COMPILED_BINDING` (cross-episode binding-keyed compilation).
- **Cost ledger** (prereg.md 11): three terms (compile, model, execution) plus a declared per-replay
  machinery term, amortized by episodes. Units are the parent's abstract units; a substrate round trip is 1
  execution unit and a model unit is 100 execution units, both inherited from the parent packet.
- **Controls** (10, prereg.md 7/8/14/15): frozen-input integrity, substrate determinism, mint
  channel, arm statelessness, parent raw-number replication, shared ground truth, positive control PC,
  negative control NC, parent baseline replication, and goal-state success. All are reported in section 5
  with PASS/FAIL and exact evidence paths.

## 4. Primary metrics (prereg.md 10)

### 4.1 Span-level action correctness, pooled over 6000 span occurrences per arm

| arm | pooled correctness (Wilson CI95) | per-rate nu=0.00, nu=0.25, nu=0.50, nu=0.75, nu=1.00 |
|---|---|---|
| `B-NO-MEMORY-DETERMINISTIC` | 0.9867 [0.9834, 0.9893] | 0.9750, 0.9750, 0.9833, 1.0000, 1.0000 |
| `B-NO-MEMORY-CONDITIONED-WIDE` | 0.8500 [0.8407, 0.8588] | 0.8500, 0.8500, 0.8500, 0.8500, 0.8500 |
| `B-NO-MEMORY-CONDITIONED-NARROW` | 0.5667 [0.5541, 0.5792] | 0.5667, 0.5667, 0.5667, 0.5667, 0.5667 |
| `B-COLD-EXPLORATION` | 1.0000 [0.9994, 1.0000] | 1.0000, 1.0000, 1.0000, 1.0000, 1.0000 |
| `WITHIN_EPISODE_SCRATCHPAD` | 1.0000 [0.9994, 1.0000] | 1.0000, 1.0000, 1.0000, 1.0000, 1.0000 |
| `CROSS_EPISODE_COMPILED_BINDING` | 1.0000 [0.9994, 1.0000] | 1.0000, 1.0000, 1.0000, 1.0000, 1.0000 |
| `WITHIN_EPISODE_SCRATCHPAD-NO-MINTFLAG` | 0.8833 [0.8750, 0.8912] | 0.8833, 0.8833, 0.8833, 0.8833, 0.8833 |

### 4.2 Class-(iii) closure rate (the mechanism under test)

| arm | pooled class-(iii) closure | nu=0.00, nu=0.25, nu=0.50, nu=0.75, nu=1.00 |
|---|---|---|
| `B-NO-MEMORY-DETERMINISTIC` | 0.8667 [0.8371, 0.8915] | 0.7500, 0.7500, 0.8333, 1.0000, 1.0000 |
| `B-NO-MEMORY-CONDITIONED-WIDE` | 0.0000 [0.0000, 0.0064] | 0.0000, 0.0000, 0.0000, 0.0000, 0.0000 |
| `B-NO-MEMORY-CONDITIONED-NARROW` | 0.0000 [0.0000, 0.0064] | 0.0000, 0.0000, 0.0000, 0.0000, 0.0000 |
| `B-COLD-EXPLORATION` | 1.0000 [0.9936, 1.0000] | 1.0000, 1.0000, 1.0000, 1.0000, 1.0000 |
| `WITHIN_EPISODE_SCRATCHPAD` | 1.0000 [0.9936, 1.0000] | 1.0000, 1.0000, 1.0000, 1.0000, 1.0000 |
| `CROSS_EPISODE_COMPILED_BINDING` | 1.0000 [0.9936, 1.0000] | 1.0000, 1.0000, 1.0000, 1.0000, 1.0000 |
| `WITHIN_EPISODE_SCRATCHPAD-NO-MINTFLAG` | 1.0000 [0.9936, 1.0000] | 1.0000, 1.0000, 1.0000, 1.0000, 1.0000 |

### 4.3 Amortized cost (units per episode)

| arm | pooled | nu=0.00, nu=0.25, nu=0.50, nu=0.75, nu=1.00 | pooled false compiled replays |
|---|---|---|---|
| `B-NO-MEMORY-DETERMINISTIC` | **40.71** | 34.08, 36.64, 40.94, 44.84, 47.06 | 80 |
| `B-NO-MEMORY-CONDITIONED-WIDE` | **48.00** | 48.00, 48.00, 48.00, 48.00, 48.00 | 0 |
| `B-NO-MEMORY-CONDITIONED-NARROW` | **48.00** | 48.00, 48.00, 48.00, 48.00, 48.00 | 0 |
| `B-COLD-EXPLORATION` | **72.00** | 72.00, 72.00, 72.00, 72.00, 72.00 | 0 |
| `WITHIN_EPISODE_SCRATCHPAD` | **48.00** | 48.00, 48.00, 48.00, 48.00, 48.00 | 0 |
| `CROSS_EPISODE_COMPILED_BINDING` | **48.20** | 48.40, 48.30, 48.20, 48.10, 48.02 | 0 |
| `WITHIN_EPISODE_SCRATCHPAD-NO-MINTFLAG` | **48.00** | 48.00, 48.00, 48.00, 48.00, 48.00 | 0 |

Paired bootstrap (5000 resamples over episodes, seed 36287182510) cost differences, units per episode:

| contrast (mean cost difference, units/episode) | nu=0.00, nu=0.25, nu=0.50, nu=0.75, nu=1.00 | two-sided bootstrap p |
|---|---|---|
| `WITHIN_EPISODE_SCRATCHPAD_minus_B-NO-MEMORY-DETERMINISTIC` | +13.92 [+12.48, +15.04], +11.36 [+10.14, +12.22], +7.06 [+6.28, +7.72], +3.16 [+2.72, +3.58], +0.94 [+0.84, +1.00] | p=0 |
| `CROSS_EPISODE_COMPILED_BINDING_minus_B-NO-MEMORY-DETERMINISTIC` | +14.32 [+13.32, +15.14], +11.66 [+10.86, +12.28], +7.26 [+6.72, +7.78], +3.26 [+2.88, +3.62], +0.96 [+0.90, +1.00] | p=0 |
| `WITHIN_EPISODE_SCRATCHPAD_minus_B-COLD-EXPLORATION` | -24.00 [-24.00, -24.00], -24.00 [-24.00, -24.00], -24.00 [-24.00, -24.00], -24.00 [-24.00, -24.00], -24.00 [-24.00, -24.00] | p=0 |
| `CROSS_EPISODE_COMPILED_BINDING_minus_B-COLD-EXPLORATION` | -23.60 [-24.00, -23.04], -23.70 [-24.00, -23.18], -23.80 [-24.00, -23.48], -23.90 [-24.00, -23.72], -23.98 [-24.00, -23.94] | p=0 |
| `WITHIN_EPISODE_SCRATCHPAD_minus_B-NO-MEMORY-CONDITIONED-WIDE` | +0.00 [+0.00, +0.00], +0.00 [+0.00, +0.00], +0.00 [+0.00, +0.00], +0.00 [+0.00, +0.00], +0.00 [+0.00, +0.00] | identical at every rate |

### 4.4 Who actually closed the class-(iii) spans (the distinction that decides clauses 2 and 3)

An arm can close a class-(iii) span in two ways: by its own declared value-retrieval mechanism, or by
deopting to the parent's perfect-policy model oracle. The two are separated here by the recorded decision
path, per span.

| arm | class-(iii) spans closed | by its OWN mechanism | by model-oracle fallback | decision paths on class-(iii) spans |
|---|---|---|---|---|
| `B-NO-MEMORY-DETERMINISTIC` | 520/600 | **0** | 520 | `COMPILED_REPLAY` 80, `DEOPT_TO_MODEL` 520 |
| `WITHIN_EPISODE_SCRATCHPAD` | 600/600 | **600** | 0 | `SCRATCHPAD_PROPAGATED` 600 |
| `CROSS_EPISODE_COMPILED_BINDING` | 600/600 | **0** | 600 | `DEOPT_TO_MODEL` 600 |

This is the most consequential table in the report. The within-episode scratchpad closed **600/600**
class-(iii) spans with its own propagated value and **0** by oracle fallback. The cross-episode
binding-keyed arm also shows 600/600, but **0** of them came from its binding-keyed cache: its
preregistered cache key contains the handle VALUE, the handle is a pure function of the episode counter,
so a class-(iii) span can never be served from cache, and every one of its class-(iii) closures was an
oracle deopt. Its 1.0000 span-level correctness is therefore inherited from the perfect-policy oracle and
is not evidence that binding-keyed compilation closes sigma_3. The ratchet's 80 errors are all false
compiled replays on class-(iii) spans.

## 5. Controls (all 10, PASS/FAIL)

| control | result | observed |
|---|---|---|
| `CTRL-FROZEN-INPUTS` | **PASS** | `all_match=True` |
| `CTRL-SUBSTRATE-IDEMPOTENCY` | **PASS** | `n_probes=8, repeats_per_probe=100, identical_round_trips=800, all_deterministic=True` |
| `CTRL-MINT-CHANNEL` | **PASS** | `{"all_passed": true, "handle_changes_with_the_counter": {"all_later_handles_are_distinct": true, "all_later_handles_differ_from_counter_1": true, "all_later_handles_match_the_declared_pure_function": true, "counter_1_handle": "00000001fac708db", "later_coun...` |
| `CTRL-ARM-STATELESSNESS` | **PASS** | `47 checks, 0 failed; GoalOnlyPlan guard present=True` |
| `CTRL-REPL-PARENT-NUMBERS` | **PASS** | `identical=True, rows=1200, field_mismatches=0; amortized cost at novelty 0.50 = 38.6 (parent 38.6); per-rate cost anchors identical = True` |
| `CTRL-SHARED-GROUND-TRUTH` | **PASS** | `{"agrees_with_reference_arm_pass": true, "every_gated_handle_equals_declared_pure_function": true, "independent_passes_agree": true, "n_gated_spans_checked": 120, "n_spans_checked": 1200, "purpose": "the single shared declared plan action (prereg.md 10) mus...` |
| `PC-PLANTED-DISAMBIGUATION` | **PASS** | `{"emitted_correct": {"B-NO-MEMORY-DETERMINISTIC": 200, "CROSS_EPISODE_COMPILED_BINDING": 200, "WITHIN_EPISODE_SCRATCHPAD": 200}, "memory_mechanism_only": {"B-NO-MEMORY-DETERMINISTIC": 0, "CROSS_EPISODE_COMPILED_BINDING": 0, "WITHIN_EPISODE_SCRATCHPAD": 0}, ...` |
| `NC-UNIQUE-STATES` | **PASS** | `{"all_rule_variants": {"authoritative_goal_aware_intent_role_arm_native_state_key": 49, "authoritative_goal_aware_intent_role_prereg13_state_key": 0, "declared_alternate_literal_rule_arm_native_state_key": 49, "declared_alternate_literal_rule_prereg13_state...` |
| `CTRL-BASELINE-REPLICATION` | **PASS** | `{"checks": {"B-COLD-EXPLORATION_cost_is_72": true, "B-COLD-EXPLORATION_span_correctness_is_1": true, "B-NO-MEMORY-CONDITIONED-NARROW_span_correctness_matches_parent": true, "B-NO-MEMORY-CONDITIONED-WIDE_cost_is_48": true, "B-NO-MEMORY-CONDITIONED-WIDE_span_...` |
| `CTRL-GOAL-STATE-SUCCESS` | **PASS** | `{"B-COLD-EXPLORATION": {"goal_state_success": 1.0, "span_level_action_correctness": 1.0}, "B-NO-MEMORY-CONDITIONED-NARROW": {"goal_state_success": 1.0, "span_level_action_correctness": 0.5666666666666667}, "B-NO-MEMORY-CONDITIONED-WIDE": {"goal_state_succes...` |

- `CTRL-FROZEN-INPUTS` — expected: recomputed sha256 of request.json / spec.json / prereg.md equal freeze.json
  - evidence: `freeze.json`, `artifacts/run_manifest.json`
- `CTRL-SUBSTRATE-IDEMPOTENCY` — expected: prereg.md 4: 8 request shapes x 100 repeats -> exactly 1 response hash and 1 status code per shape
  - evidence: `artifacts/substrate_idempotency.json`
- `CTRL-MINT-CHANNEL` — expected: prereg.md 5 and no-go 6: the mint response BODY carries capability_handle, the non-mint body is unchanged, and the handle is a pure function of (MINT_SALT, episode counter)
  - evidence: `artifacts/mint_channel_check.json`
- `CTRL-ARM-STATELESSNESS` — expected: prereg.md 6.1: 14 statelessness checks, 0 failures, plus the GoalOnlyPlan AttributeError guard; no-go 5
  - evidence: `artifacts/scratchpad_statelessness_test.json`, `artifacts/conditioned_arm_statelessness_test.json`
- `CTRL-REPL-PARENT-NUMBERS` — expected: prereg.md 15.2 / no-go 2: byte-identical per-span replication of the parent reference arm on the parent-identical generator (class_iii=False), and the parent cost anchor 38.6 at novelty 0.50
  - evidence: `artifacts/replication_parent_comparison.json`, `artifacts/spans_REPL-REFERENCE-PARENT-IDENTICAL.jsonl`, `artifacts/replication_parent_numbers.json`
- `CTRL-SHARED-GROUND-TRUTH` — expected: prereg.md 10: the declared plan action bound at execution time is identical for every arm and reproducible
  - evidence: `artifacts/shared_ground_truth_integrity.json`
- `PC-PLANTED-DISAMBIGUATION` — expected: prereg.md 7 / no-go 3: the scratchpad and the cross-episode compiled arm must close 200/200 planted spans; the ratchet compiles 0/200 because the state key is identical
  - evidence: `artifacts/pc_verification.json`, `artifacts/classification_PC-PLANTED-DISAMBIGUATION.jsonl`
- `NC-UNIQUE-STATES` — expected: prereg.md 8 / no-go 4: sigma_2 == 0 exactly under the authoritative goal-aware rule with the literal prereg.md 13 mechanism, and no span is labelled class (ii) under any rule variant
  - evidence: `artifacts/nc_verification.json`, `artifacts/classification_NC-UNIQUE-STATES-authoritative_goal_aware_intent_role_prereg13_state_key.jsonl`
- `CTRL-BASELINE-REPLICATION` — expected: the four inherited parent arms reproduce their parent-packet values (ratchet 0.9833 span-level correctness and 40.94/34.08/36.64/44.84/47.06 amortized cost with the plant, conditioned 0.8500 at 48.0, narrow 0.5667, cold 1.0 at 72.0, and 30/30/20/0/0 false compiled replays)
  - evidence: `artifacts/baseline_replication.json`
- `CTRL-GOAL-STATE-SUCCESS` — expected: every arm reaches goal-state success 1.0 (the parent's invariant); any arm below is an instrument failure
  - evidence: `artifacts/goal_state_success.json`
  - caveat: goal-state success is blind to a missing binding key; it is reported only as a blindness demonstration, never as a quality measure

## 6. The residual decomposition, and the one measurement definition that moves it

The three new arms emit the *declared* action on the reference's task instances, so the reference trace's
wrong spans are the residual, and the classes are properties of the reference trace, not of any arm. Under
the authoritative goal-aware rule (state key recurs with a different correct action **for the same goal
intent**, where the goal intent is the `intent` field of the goal prefix, which the generator itself sets to
the role):

| sigma | pooled (Wilson CI95) | nu=0.00, nu=0.25, nu=0.50, nu=0.75, nu=1.00 |
|---|---|---|
| sigma_1 merely novel | 0.6772 [0.6652, 0.6889] | 0.6233 [0.5956, 0.6503], 0.6483 [0.6209, 0.6748], 0.6783 [0.6514, 0.7042], 0.7017 [0.6752, 0.7269], 0.7342 [0.7085, 0.7584] |
| sigma_2 epistemically blocked | 0.2228 [0.2125, 0.2335] | 0.2767 [0.2521, 0.3027], 0.2517 [0.2279, 0.2770], 0.2217 [0.1991, 0.2460], 0.1983 [0.1768, 0.2218], 0.1658 [0.1459, 0.1879] |
| sigma_3 observation absent | 0.1000 [0.0927, 0.1078] | 0.1000 [0.0843, 0.1183], 0.1000 [0.0843, 0.1183], 0.1000 [0.0843, 0.1183], 0.1000 [0.0843, 0.1183], 0.1000 [0.0843, 0.1183] |
| headroom (sigma_2 + sigma_3) | 0.3228 [0.3111, 0.3348] | 0.3767 [0.3497, 0.4044], 0.3517 [0.3252, 0.3791], 0.3217 [0.2958, 0.3486], 0.2983 [0.2731, 0.3248], 0.2658 [0.2416, 0.2915] |

Three operationalisations of the *same frozen sentence* on the *same data*:

| rule | pooled sigma_2 | per-rate sigma_2 (counts of class ii) |
|---|---|---|
| authoritative_goal_aware_intent_role | 0.2228 | 332, 302, 266, 238, 199 |
| declared_alternate_literal_step2 | 0.2228 | 332, 302, 266, 238, 199 |
| declared_alternate_prefix_intent | 0.0800 | 191, 143, 97, 49, 0 |

**The measured result is that the authoritative goal-aware rule and the inherited literal rule are
numerically identical here: sigma_2 = 0.2228 versus 0.2228 pooled (1337/6000 each).** Only the
strictest full-prefix intent reading differs, at 0.0800 (480/6000). The reason is mechanical: the
arm-native observable state key already contains the executor's own last request, so it already separates
the roles that the `intent` field would separate, and conditioning on `intent` therefore adds nothing. The
same identity holds in the NC control (49/1200 under both rules with the arm-native state key). What
actually moves sigma_2 in this experiment is the choice of STATE KEY, not the choice of intent rule, and
that is reported rather than assumed. Clause 1 fails by a wide margin under all three readings, so no
reading of the frozen rule rescues it. Every headroom number in the program nonetheless inherits this
choice, and this experiment cannot settle it from its own data.

## 7. Positive control PC-PLANTED-DISAMBIGUATION (prereg.md 7, no-go 3)

- protocol: prereg.md 7: 200 create_resource span occurrences, all issued from (empty store, last_request=GET /) with 4 different resource identities, so the correct action is goal-distinct but the observation is identical
- 200 planted `create_resource` span occurrences; observation-identical within each episode: **True**; 4 distinct correct actions per episode: **True**
- planted span classes under the authoritative rule: {'i': 1, 'ii': 199, 'iii': 0}
- prereg expected: scratchpad_closure = 200/200, compiled_closure = 200/200, ratchet_closure = 0/200

| arm | emitted-correct closure | closed by the memory mechanism itself |
|---|---|---|
| `WITHIN_EPISODE_SCRATCHPAD` | 200/200 | 0/200 |
| `CROSS_EPISODE_COMPILED_BINDING` | 200/200 | 0/200 |
| `B-NO-MEMORY-DETERMINISTIC` | 200/200 | 0/200 |

**Both readings are reported because the prereg string (scratchpad_closure = 200/200, compiled_closure = 200/200, ratchet_closure = 0/200) is only simultaneously
attainable under a mechanism reading for the ratchet.** Under the literal prereg sentence — a planted span is
closed iff the emitted `(method, path, body)` equals the declared plan action — all three arms close the
planted spans, including the ratchet, because an ungated planted span never needs a binding. The PC
therefore verifies that the plant really is observation-identical, not that value propagation is needed
for it. `no_go_3` is gated on the literal reading (200/200 for both new arms) and the mechanism reading is
reported alongside. This is disclosed rather than silently resolved in either direction.

## 8. Negative control NC-UNIQUE-STATES (prereg.md 8/13, no-go 4)

- protocol: prereg.md 8 and 13: every span carries a uniqueness nonce appended to the WORLD STORE SNAPSHOT (part of the declared observable state), not to the request path where the inherited generator put it
- prereg criterion: sigma_2 == 0 under the authoritative goal-aware rule with the literal prereg.md 13 mechanism (no-go 4) -> sigma_2 count **0** (n = 1200 span occurrences)

| rule variant | unique state keys | sigma_2 count (share) | sigma_3 count (share) |
|---|---|---|---|
| authoritative_goal_aware_intent_role_prereg13_state_key | 1200 | 0/1200 (0.0000) | 0/1200 (0.0000) |
| authoritative_goal_aware_intent_role_arm_native_state_key | 1151 | 49/1200 (0.0408) | 0/1200 (0.0000) |
| declared_alternate_literal_rule_arm_native_state_key | 1151 | 49/1200 (0.0408) | 0/1200 (0.0000) |
| declared_alternate_literal_rule_prereg13_state_key | 1200 | 0/1200 (0.0000) | 0/1200 (0.0000) |
| declared_alternate_prefix_intent_prereg13_state_key | 1200 | 0/1200 (0.0000) | 0/1200 (0.0000) |

Interpretation: MEASURED, and it is the STATE KEY that decides this control, not the class-(ii) rule. With the prereg.md 13 mechanism the nonce makes every world-store key unique (1200/1200), so sigma_2 is exactly 0 under all three rule variants. With the arm-native key, which ignores the nonce in the request path, sigma_2 is 49/1200 under BOTH the inherited literal rule and the authoritative goal-aware (intent=role) rule, which agree exactly. The parent's NC residual of 49/1200 is therefore reproduced here by the arm-native state key alone, and the class-(ii) rule has no effect on it in either direction. The goal-aware rule is also indistinguishable from the literal rule on the main grid (both 1337/6000): the arm-native state key already contains the executor's last request, so it already separates the roles the intent field would separate. Only the strictest full-prefix intent reading changes the count (480/6000).

The same control also produces a **measured instrument result that is not a memory result**, and it is
reported here so that it cannot be misread as one:

| NC arm | span-level action correctness | reads the plan action? |
|---|---|---|
| reference ratchet | 1.0000 | yes |
| inherited cold | 1.0000 | yes |
| new compiled binding | 1.0000 | yes |
| new scratchpad | 0.0000 | no (reconstructs from the goal prefix) |
| inherited conditioned wide | 0.0000 | no (reconstructs from the goal prefix) |

Why: in this control the inherited generator helper taskplan._with_nonce appends '?n=<episode>-<step>' to EVERY path, including '/'. The declared goal prefixes (wide, wide_mint, narrow) do not carry the path, so any arm that reconstructs its request from the prefix alone cannot reproduce the nonce. The NEW scratchpad and the INHERITED
conditioned arm collapse identically, while the ratchet, the cold arm and the new compiled arm do not, so
the collapse tracks the prefix's coverage of the request rather than memory scope. `no_go_4` is a
criterion on the classifier's labels and is evaluated on the labels alone.

## 9. Endpoints that could not have answered the question

| arm | goal-state success (pooled) | span-level action correctness (pooled) |
|---|---|---|
| `B-NO-MEMORY-DETERMINISTIC` | 1.0000 | 0.9867 [0.9834, 0.9893] |
| `B-NO-MEMORY-CONDITIONED-WIDE` | 1.0000 | 0.8500 [0.8407, 0.8588] |
| `B-NO-MEMORY-CONDITIONED-NARROW` | 1.0000 | 0.5667 [0.5541, 0.5792] |
| `B-COLD-EXPLORATION` | 1.0000 | 1.0000 [0.9994, 1.0000] |
| `WITHIN_EPISODE_SCRATCHPAD` | 1.0000 | 1.0000 [0.9994, 1.0000] |
| `CROSS_EPISODE_COMPILED_BINDING` | 1.0000 | 1.0000 [0.9994, 1.0000] |
| `WITHIN_EPISODE_SCRATCHPAD-NO-MINTFLAG` | 1.0000 | 0.8833 [0.8750, 0.8912] |

Goal-state success is 1.0 for every arm, including arms that are wrong on a fifth of their spans, because
the substrate accepts `PUT /resources/{rid}` where the handle must be bound. It is reported as a measured
blindness demonstration, never as a quality measure — and it is the reason the primary endpoint was
replaced before this experiment ran.

## 10. Validity threats and frozen representation loss

- REPRESENTATION LOSS (frozen, DI-01): the scratchpad arm and its no-mint-flag sensitivity are conditioned on goal_prefix_wide_mint, i.e. the parent's frozen 7-field wide prefix plus exactly one field, mint={0|1}. Without it a scratchpad that emits the ungated create never receives a handle. The handle VALUE is in no prefix, and wide and narrow are byte-identical to the parent, so the inherited conditioned baselines are unchanged. The price of the flag is measured, not argued: see metrics.declared_instrument_deviation_DI_01_mint_flag.
- REPRESENTATION LOSS (frozen): the capability handle is returned in the mint response BODY in addition to the header. Every non-mint response body is byte-identical to the parent's, which is what keeps CTRL-REPL-PARENT-NUMBERS exact; the mint response body differs from the parent's by exactly one field.
- CLASS-(ii) RULE (frozen, authoritative): the goal-aware reading is implemented as state key + the `intent` field of the goal prefix, which the generator itself names `intent` and sets to the role. Two declared alternates are reported in metrics.class_ii_rule_operationalisations. MEASURED RESULT: the authoritative goal-aware rule and the inherited literal rule are NUMERICALLY IDENTICAL on this data (1337/6000 pooled; 49/1200 in NC under the arm-native state key), because the arm-native state key already contains the executor's own last request and therefore already separates the roles the intent field would separate. Only the strictest full-prefix intent reading differs (480/6000). The choice of STATE KEY, not the choice of intent, is what moves sigma_2 in this experiment. The clause-1 test consumes the authoritative value, and clause 1 fails by a wide margin under all three readings (CI95 upper 0.19-0.30 at every rate).
- FROZEN-IMPLEMENTATION DISCREPANCY, REPORTED NOT REPAIRED: prereg.md 6.3 describes B-NO-MEMORY-DETERMINISTIC as compiling 'within episode only, no cross-episode retention', but the frozen unmodified arm keeps its compiled cache on the instance across all 50 episodes of a run (arms/deopt_ratchet.py, run_episode never clears self.cache). The new cross-episode arm therefore differs from the reference arm in the binding key and in the declared machinery term rather than in retention alone. The arm was not modified, because the prereg declares it the unmodified parent reference and its measured values are the frozen anchors.
- BOUNDED INFORMATION FLOW, DECLARED: the cross-episode arm reads the BOOLEAN 'is this plan step capability-gated' from the plan step it is already required to materialise (the parent's arm contract consumes that step for the expected role and status code). It never reads the handle value from the plan; the handle it keys on is the one it induced from its own response body. An audit field records whether the arm's own induced binding equals the handle the plan bound, for every gated span.
- ORACLE-MEDIATED CLOSURE, MEASURED AND MATERIAL: the cross-episode binding-keyed arm reaches class-(iii) closure 1.0000, but 0 of its 600 class-(iii) closures came from its own binding-keyed cache; every one was a DEOPT_TO_MODEL fallback, because its preregistered cache key contains the handle VALUE and the handle is a pure function of the episode counter, so a class-(iii) span can never be served from cache. Its 1.0000 span-level correctness is therefore inherited from the perfect-policy oracle and is NOT demonstrated by binding-keyed compilation. The within-episode scratchpad's class-(iii) closure is NOT oracle-mediated: 600/600 came from its own propagated value. The ratchet's class-(iii) closure is 0.8667 (0 by its own compiled replay) and its failures are exactly its false compiled replays. Any reading of clause 3 that treats 1.0000 as evidence that binding-keyed compilation closes sigma_3 is unsupported by this run.
- The model oracle is the parent's perfect-policy stand-in and is given the plan (arms/common.py ModelOracle). Both new arms may deopt to it, exactly as the reference arm does. The scratchpad arm never calls it for content: its decision function is total, and its 1 model unit per span is a ledger charge for a per-span policy decision, identical to the conditioned baseline's. The parenthetical reading of prereg.md 6.1 ('model unit per span for spans not resolved from scratchpad') is reported as the sensitivity in metrics.
- The generator's declared class_iii_fraction=0.10 is realised exactly (120 of 1200 span occurrences), and class-(iii) membership is VERIFIED per span (the handle is checked absent from the observable state and from both goal prefixes) rather than assumed from the plant schedule.
- The PC population is ungated by construction, so the PC tests goal disambiguation of observation-identical spans, not binding-value propagation; the mechanism-only closure reading is reported for all three arms so this is visible rather than hidden.
- INHERITED THRESHOLD PROVENANCE, DISCLOSED: the 0.9833 correctness threshold is the parent packet's headline figure for the reference arm, which is that packet's NOVELTY-0.50 RATE; the parent's POOLED value over all five rates, recomputed here from the parent's own raw span artifact, is 5920/6000 = 0.986667. Both new arms are 1.0000 at every rate, so clause 2 leg (a) and clause 3 leg (a) hold under either reading; the threshold is inherited unchanged and not re-derived here. The reference arm's per-rate and pooled correctness reproduce the parent artifact EXACTLY (see metrics.controls.CTRL-BASELINE-REPLICATION).
- SUBSTRATE-CHANGE CONDITIONALITY, INHERITED FROM THE PARENT AUDIT (this is the load-bearing caveat of the whole experiment): the parent packet's audit recorded that on the parent substrate the capability handle was returned only in a response HEADER, which was not a declared readable channel, and that therefore no real model could have read it from the declared channels. This experiment's frozen modification (prereg.md 4 and 5) returns the handle in the mint response BODY as the field capability_handle. CONSEQUENCE: BOTH new arms are measurable ONLY because of that modification. On the unmodified parent substrate neither the scratchpad nor the compiled arm could have observed any handle value to propagate or key on, so both arms would have been unable to close any class-(iii) span by their own mechanism. These results therefore measure value propagation GIVEN a readable handle channel, and they do NOT establish what an executor without that channel can do, nor that a real substrate exposes handles readably. Disclosed as a frozen representation loss; not repaired, not generalised.
- ARMS ARE DETERMINISTIC RULES, NOT LANGUAGE MODELS, INHERITED FROM THE PARENT AUDIT: every arm in this run, new and inherited alike, is a deterministic policy rule with programmatic access to the declared plan through the parent ModelOracle stand-in in arms/common.py. The correctness, class-closure and headroom numbers are therefore UPPER BOUNDS on the information available to a policy that can read the observable channels and the declared goal prefix; they are not predictions of language-model behaviour, they do not measure a model's ability to hold, notice or propagate a value across a context window, and the abstract-unit costs carry no token, latency or dollar mapping. No real Web work, no real model, and no real inheritance mechanism is exercised anywhere in this run.
- INHERITED-AUDIT DISPOSITION (parent EXP-FRONTIER-36272394045 audit.json, status REVISE, producer_claim_supported=false, 8 required_fixes), recorded so this packet is self-contained: (UR-04 cost basis) resolved before freeze in spec.json decision_rule.cost_basis, binding the parent's three-term compile+model+execution ledger, the basis the 38.6 threshold was derived on; (UR-01 clause-1 label conflict) resolved before freeze in spec.json decision_rule.clause_1_label as RESIDUAL_NOT_ZERO, replacing the parent's contradictory FALSIFIES_INHERITANCE_NICHE mapping; (UR-02 class-(ii) ambiguity) resolved before freeze by declaring the goal-aware reading authoritative with the literal reading rejected-with-reason, and all three operationalisations are reported here as metrics.class_ii_rule_operationalisations; (NC mechanism) FIXED as required, the uniqueness nonce is placed in the world-store snapshot per prereg.md 13 rather than in the request path, and sigma_2 is then exactly 0; (PC class assignment) addressed by reporting the PC's planted span classes under the authoritative rule and disclosing that the PC population is ungated, so it cannot discriminate the class-(ii) reading; (reference arm false compiles) acknowledged and quantified here, 80 class-(iii) false COMPILED_REPLAY decisions, in every cost comparison; (conditioned arm is a deterministic rule with oracle access) and (goal-state success is insensitive) both carried forward and restated above and in metrics.controls.CTRL-GOAL-STATE-SUCCESS. This run does not itself resolve the parent's documentary cost-basis dispute, it inherits the parent's adjudication of it.
- Single machine, stdlib ThreadingHTTPServer on 127.0.0.1, no browser, no docker, no model API key, no network. Wall clock and request counts are in artifacts/run_manifest.json.

### 10.1 Disposition of the parent auditor's required fixes

Parent `EXP-FRONTIER-36272394045` closed at `audit_status=REVISE` with `producer_claim_supported=false` and 8 `required_fixes`. This run is a DIRECT response to that audit, so the disposition is recorded here rather than left for the reader to reconstruct:

| parent required_fix | disposition in this packet |
|---|---|
| UR-04: cost basis ambiguity flips clause 2 | RESOLVED BEFORE FREEZE in `spec.json` `decision_rule.cost_basis`: the parent's three-term compile+model+execution ledger, the basis on which 38.6 was derived. The parent's documentary dispute is inherited, not reopened. |
| UR-01: clause-1 label asserts the opposite of the prose | RESOLVED BEFORE FREEZE in `spec.json` `decision_rule.clause_1_label`: `RESIDUAL_NOT_ZERO`, replacing `FALSIFIES_INHERITANCE_NICHE`. |
| UR-02: class-(ii) literal vs goal-aware | RESOLVED BEFORE FREEZE: goal-aware declared authoritative, literal rejected with reason; all three operationalisations reported in section 6. |
| NC must place the nonce in the world-store snapshot | FIXED as required (`prereg.md 13` mechanism, `prereg13_state_key`): 1200/1200 unique keys, sigma_2 exactly 0. See section 8. |
| PC class assignment must match the chosen reading | ADDRESSED AND DISCLOSED: the PC population is ungated, so under the literal emitted-correct reading all three arms close 200/200; mechanism-only closure is reported for all three. See section 7. |
| Reference arm's 80 class-(iii) false compiles | ACKNOWLEDGED AND QUANTIFIED in every cost comparison: 80 false `COMPILED_REPLAY` decisions, all `list_resources`, all class-(iii). See sections 4.3, 4.4, 13. |
| The conditioned arm is a deterministic rule with oracle access, not a model; the substrate never returns the handle in a body | CARRIED FORWARD AND EXTENDED: validity note 'ARMS ARE DETERMINISTIC RULES, NOT LANGUAGE MODELS', plus the new substrate-change conditionality note below. |
| Goal-state success is insensitive (1.0 even at 0.5667 span correctness) | CARRIED FORWARD: section 9 measures the blindness directly; the endpoint was replaced before freeze for exactly this reason. |

### 10.2 The load-bearing caveat: the parent substrate never exposed the handle readably

The parent audit recorded that on the parent substrate the capability handle was returned only in a
response **header**, which was not a declared readable channel, and that therefore no real model could
have read it from the declared channels. This experiment's frozen modification (prereg.md 4/5) returns
the handle in the mint response **body** as `capability_handle`.

**Both new arms are measurable only because of that modification.** On the unmodified parent substrate
neither arm could have observed any handle value to propagate or key on, so neither could have closed a
single class-(iii) span by its own mechanism. These results measure value propagation *given* a readable
handle channel. They do not establish what an executor without that channel can do, nor that a real
substrate exposes handles readably. This is a frozen representation loss, disclosed and not repaired.

## 11. What is NOT concluded

- No claim that within-episode value propagation is sufficient to close the residual as a class of agent architectures: only two arms on one plan family on one substrate were measured.
- No claim that persistent cross-episode inheritance is unnecessary. The producer does not self-promote; the frozen scope verdict is reported as measured and adjudicated by the Director.
- No claim that goal-state success is a valid endpoint; it is reported here only as a measured blindness demonstration.

## 12. Open questions for the Director

- Is the class-(ii) rule a measurement definition to be fixed once for the program, or a per-experiment choice? Three readings of the same frozen text give sigma_2 between 0.08 and 0.22283333333333333 on identical data, and every downstream headroom number inherits that choice.
- Should a binding-IDENTITY cache key (the identity of the capability, not its episode-scoped value) be preregistered next? This run MEASURED that the preregistered binding-VALUE key produced 0/600 class-(iii) closures from its own cache and that the arm's 1.0000 correctness was entirely oracle-mediated, so this is no longer a hypothetical.
- The cost leg of BOTH clauses failed at a specific point: the scratchpad's 48.00 units/episode is the SAME ledger as the inherited conditioned baseline's 48.00, and the frozen 38.6 bar is the inherited ratchet's amortized cost. Should the economic bar for any successor be re-derived, or is 38.6 the program's standing bar? This run inherited the threshold unchanged and cannot answer whether the bar or the measurement is the right target.

## 13. Run facts

- wall clock 31.22 s; 58425 substrate requests across every pass (determinism probe, mint channel, arm grid, parent replication, two independent ground-truth passes, PC, NC)
- main grid: 7 arms x 250 episodes x 24 spans = 42000 span occurrences; every arm saw byte-identical task instances (novelty rates 0.00/0.25/0.50/0.75/1.00, 50 episodes per rate)
- artifacts: 126 files under `research/experiments/EXP-FRONTIER-36287182510/artifacts/`, each with a SHA-256 in `result.json.artifacts` (verified against the files on disk at write time)
- 80 false compiled replays across all five rates for the reference arm; headroom closed by the scratchpad: nu=0.00 1.0000, nu=0.25 1.0000, nu=0.50 1.0000, nu=0.75 1.0000, nu=1.00 1.0000
