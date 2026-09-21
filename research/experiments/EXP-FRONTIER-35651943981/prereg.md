# EXP-FRONTIER-35651943981 — Preregistration

## Status

DESIGN NOT YET FROZEN.

## 1. Claim

**C-RESIDUAL-NOVELTY**: Later-agent cost tracks residual novelty rather than full task length.

- Status: HYPOTHESIS (0 prior experiments)
- Owner lanes: graph, product
- Frontier's role: test the claim in a controlled synthetic testbed (Frontier's charter: search outside current solution basin for high-upside falsifiable mechanisms)

## 2. Scientific Question

Does later-agent cost track residual novelty fraction rather than full task length, when task length and novelty fraction are independently controlled in a synthetic web-like testbed?

## 3. Hypothesis

The cost advantage of mechanism inheritance over cold exploration is negatively correlated with novelty fraction (Spearman rho < 0) and is not positively correlated with task length when novelty fraction is held constant.

Specific sub-hypotheses:

- H1: At 0% novelty, inheritance provides negligible advantage over cold (cost_advantage <= 0.15).
- H2: At 100% novelty, inheritance provides no advantage (cost_advantage < 0.10).
- H3: cost_advantage is monotonically decreasing in novelty fraction (Spearman rho < -0.5).
- H4: At fixed novelty fraction, cost scales with novelty fraction, not with task length (no significant correlation between cost and task length within novelty strata).

## 4. Falsifier

The hypothesis is FALSIFIED if any of:

- (a) Spearman rho(cost_advantage, novelty_fraction) >= 0 (positive or zero correlation);
- (b) Spearman rho(cost_advantage, task_length) is significant and negative at fixed novelty fraction (cost tracks task length, not novelty);
- (c) cost_advantage at 0% novelty exceeds 0.15 (inheritance helps when nothing is new — spurious mechanism);
- (d) cost_advantage at 100% novelty exceeds 0.10 (inheritance helps when everything is new — mechanism is not novelty-dependent).

## 5. Synthetic Testbed Design

### 5.1 Environment

A simulated web application with:

- **State space**: 20 pages, each with a form requiring 1-5 parameter fields.
- **Action vocabulary**: navigate(page_id), fill(field, value), submit(form), click(button).
- **Parameter values**: Pool of 100 possible values per field (product IDs, quantities, names, etc.).
- **Transitions**: Deterministic given (state, action): fill(field, value) updates the form state; submit(form) navigates to confirmation; navigate(page_id) changes page.

### 5.2 Task Generation

A task is a sequence of actions to reach a target state (e.g., "add product X with quantity Y to cart and checkout").

**Task length** (independent variable): 3, 6, or 9 actions.

**Novelty fraction** (independent variable): 0%, 25%, 50%, 75%, 100%.

Novelty fraction = (number of action-parameter values not in training set) / (total parameter values in task).

### 5.3 Training Set

The first agent generates 50 trajectories through the testbed, covering 15 of the 20 pages and 60 of the 100 parameter values per field. This creates a partial but non-trivial training set.

### 5.4 Test Grid

| Novelty | Length=3 | Length=6 | Length=9 |
|---------|----------|----------|----------|
| 0%      | 10 tasks | 10 tasks | 10 tasks |
| 25%     | 10 tasks | 10 tasks | 10 tasks |
| 50%     | 10 tasks | 10 tasks | 10 tasks |
| 75%     | 10 tasks | 10 tasks | 10 tasks |
| 100%    | 10 tasks | 10 tasks | 10 tasks |

Total: 150 task instances × 4 conditions × 5 reps = 3000 runs.

### 5.5 Cost Proxy

Since this is a synthetic testbed without real LLM calls, cost is proxied by:

- **action_count**: Number of actions the second agent takes to complete the task.
- **novel_action_count**: Number of actions not in the training set (requires exploration).
- **decision_points**: Number of choice points where the agent must decide what to do next.

The primary cost metric is `action_count` (lower is better). `novel_action_count` is the secondary metric.

For real-LLM validation, the cost proxy is validated against actual token count in a small pilot (10 tasks per condition) using a fixed LLM model. The proxy-to-real correlation must exceed 0.7 for the proxy to be valid.

## 6. Conditions

### 6.1 B-COLD (Cold Start)

Second agent starts with no prior knowledge. It must explore the testbed from scratch to complete each task.

- No access to training trajectories.
- No access to SPIDER mechanisms.
- Uses the same action vocabulary and budget as other conditions.

**Expected**: Cost scales with task length; no novelty-dependent benefit.

### 6.2 B-REPLAY (Exact Replay)

Second agent replays the exact action sequence from the matching training trajectory.

- Training trajectories are matched by task description similarity.
- If the test task has identical parameter values to a training task, replay succeeds.
- If parameter values differ, replay fails at the first mismatch.

**Expected**: Near-zero cost at 0% novelty; fails at >0% novelty.

### 6.3 B-RETRIEVAL (Retrieval-Based)

Second agent retrieves the most similar prior trajectory by task description similarity (TF-IDF cosine) and adapts it.

- Retrieves top-1 most similar training trajectory.
- Attempts to adapt parameter values using string matching and template substitution.
- No parameterized mechanism induction.

**Expected**: Partial benefit at low novelty; degrades with novelty; better than cold at moderate novelty.

### 6.4 B-SPIDER-PARAM (SPIDER Parameterized Inheritance)

Second agent uses SPIDER's parameterized mechanism pipeline:

1. **distill_parameterized()**: From 50 training observations, induce parameterized mechanisms with parameter slots.
2. **resolve()**: Given the new task description, resolve to the best-matching mechanism.
3. **bind()**: Fill parameter slots with new task-specific values.
4. **execute()**: Execute the bound mechanism in the testbed.
5. **verify()**: Check postconditions.

This uses the actual SPIDER kernel code path (src/spider/kernel.py).

**Expected**: Strong benefit at low novelty (parameter binding works); degrades with novelty fraction.

## 7. Metrics

### Primary

- **cost_advantage**: (B-COLD action_count - B-SPIDER-PARAM action_count) / B-COLD action_count. Positive means inheritance helps.

### Secondary

- **cost_advantage_retrieval**: (B-COLD action_count - B-RETRIEVAL action_count) / B-COLD action_count.
- **task_success_rate**: Fraction of tasks completed successfully per cell.
- **novel_action_count**: Number of actions not in training set per condition.
- **action_count_by_condition**: Raw action counts for each condition per cell.

### Derived

- **rho_novelty**: Spearman correlation between cost_advantage and novelty_fraction (primary test statistic).
- **rho_length**: Spearman correlation between cost_advantage and task_length within each novelty stratum.

## 8. Decision Rule

### SURVIVES_CURRENT_TEST if ALL:

1. **Novelty correlation**: Spearman rho(cost_advantage_spider, novelty_fraction) < 0 with permutation p < 0.05 (N=1000 permutations over task instances).
2. **Length independence**: Spearman rho(cost_advantage_spider, task_length) is NOT significant (p >= 0.05) when novelty fraction is held constant within each novelty level.
3. **Null control**: cost_advantage at 0% novelty <= 0.15.
4. **Positive control**: cost_advantage at 0% novelty > 0.20 AND cost_advantage at 100% novelty < 0.10 AND rho_novelty < -0.5.

### FALSIFIED if ANY:

- rho_novelty >= 0 or permutation p >= 0.05 (condition 1 fails).
- rho_length is significant and negative within fixed novelty (condition 2 fails).
- Null control fails (cost_advantage at 0% > 0.15).
- Positive control fails (any sub-condition).

### MEASUREMENT_INVALID if:

- >30% task failure rate in any cell across all conditions.
- Independence of novelty fraction and task length is violated (confounded design).
- Cost proxy validation correlation < 0.7.

## 9. Controls

| Control | Identifier | Expected | Pass Criterion |
|---------|-----------|----------|----------------|
| Positive: novelty gradient | PC-NOVELTY-GRADIENT | Monotonic decrease | rho < -0.5, p < 0.05, 0% > 0.20, 100% < 0.10 |
| Null: zero novelty | NC-ZERO-NOVELTY | No advantage | cost_advantage(0%) <= 0.15 |
| Replay baseline | B-REPLAY | Exact match cost | action_count ~ task_length at 0% novelty |
| Task independence | TI-INDEPENDENCE | Orthogonal design | No significant correlation (r < 0.1) between novelty_fraction and task_length in generated tasks |

## 10. Validity Threats

1. **Cost proxy validity**: Action count may not correlate with real LLM token cost. Mitigated by pilot validation (section 5.5).
2. **Task representativeness**: Synthetic testbed may not reflect real web task structure. Claim ceiling bounded to synthetic testbed.
3. **Mechanism quality**: distill_parameterized() may produce poor mechanisms on limited training data (50 trajectories). This is a genuine test of the mechanism, not a flaw.
4. **Retrieval baseline strength**: TF-IDF retrieval may be too weak; a stronger retrieval baseline (e.g., embedding similarity) could change the comparison. Acceptable for POC.
5. **Novelty fraction computation**: The definition of "novel parameter value" depends on training set coverage. Different training sets could shift the novelty gradient.

## 11. Scope and Claim Ceiling

- **Claim ceiling**: Synthetic web-like testbed with deterministic transitions, 20 pages, 100 values/field, 50 training trajectories.
- **Not tested**: Real web pages, real LLM agents, browser interaction, network latency, authentication, multi-tab navigation, JavaScript rendering.
- **Not promoted**: No product promotion from this experiment. If SURVIVES, the next step is real-LLM validation (C-LLM-INHERIT).
- **Cross-lane**: This experiment tests the economic thesis (C-RESIDUAL-NOVELTY). It does not test C-WEB-DYNAMICS, C-PARAM-INHERIT kernel integration, or C-CROSSSITE. Those remain separate.

## 12. Consequences

### If SURVIVES

- C-RESIDUAL-NOVELTY advances from HYPOTHESIS toward EXPERIMENTAL.
- Product economic thesis validated in synthetic setting.
- Justifies real-LLM cost measurement (C-LLM-INHERIT).
- Frontier's PIVOT from C-WEB-DYNAMICS is justified: the economic thesis is higher leverage than estimator refinement.

### If FALSIFIED

- C-RESIDUAL-NOVELTY is rejected in synthetic setting.
- Product economic thesis undermined: later-agent cost does not track residual novelty.
- Product should pivot from mechanism inheritance toward alternative value propositions.
- Resources shift to C-FRESHNESS, C-DELTA-REPAIR, or other priority claims.

### If MEASUREMENT_INVALID

- No valid inference about C-RESIDUAL-NOVELTY.
- Investigate measurement failure and design corrected experiment.
