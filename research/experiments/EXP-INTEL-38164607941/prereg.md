# EXP-INTEL-38164607941 preregistration

Lane: `intel` — design_contract_version 2
Status: **DESIGN — NOT YET FROZEN**

Parent experiment: EXP-INTEL-37982024058 (FALSIFIES; audit PASS).
Parent handoff: `research/experiments/EXP-INTEL-37982024058/handoff.json`, sha256 `b2aee1adb07ba2e5aaa5096cd5ca3b7c630398f600ce33210320321c882d1a55`.
Director mandate: `request.json#director_mandate` (allocation CONTINUE, claim `C-LLM-INHERIT`, `parent_handoff_disposition: SUPERSEDE`, `cognitive_reset: true`).
Resumed pre-freeze sibling: EXP-INTEL-38123995594 (never froze; its only failure was the shared design-review model outage, fingerprint `3b9ff5e4e9e73f23e368efb4`).

---

## 1. Question

Under the same credential-free, CPU-quantized constraints as EXP-INTEL-37982024058 (identical minimal task, GBNF grammar, sampling, seeds, model artifacts, scorer and configuration), does supplying the task goal and action schema in the system prompt — condition **P-TREAT-GOAL-SCHEMA**, derived from the grandparent harness SYS prompt (`research/experiments/EXP-INTEL-37973264582/raw/code/min_webagent.py`, file sha256 `4e2b6710c78f4e4399a8ed5ae78e0231563fb832b780b80a955bcbc16b046862`, SYS string sha256 `742e5aae5b5ffd72ccb43cb18658a14483660e7659640df651e91011e9b6dc12`) with one ref→selector schema alignment (adapted string sha256 `36a4240aba96e46797c16aebbedcc548778a0c1097b4ce4432608148758c5716`) — convert M-7B-QWEN's or M-3B-QWEN's step-0 reveal-click into a full click-then-answer completion, where the ONLY varied dimension between treatment and comparator cells is `prompts.system`?

This is the Director's binding strategic question. It is a refinement into the smallest rigorous falsifiable probe (a single-factor paired prompt ablation), not a substitute objective.

## 2. Hypotheses

- **H1 (capability).** At least one of M-7B-QWEN (evaluated first) or M-3B-QWEN clears the pre-declared capability bar (`task_success_rate >= 0.6` AND `parseable_action_rate_step1 >= 0.6` over the 5 frozen seeded episodes) under P-TREAT-GOAL-SCHEMA, converting the parent FALSIFIES (bounded by audit VF-01 to the underspecified-prompt ceiling) into SUPPORTS at the goal/schema protocol ceiling.
- **H1b (attribution).** For each clearing candidate, the contemporaneous within-experiment paired comparator cell under P-COMP-UNDERSPECIFIED (byte-identical to the parent system prompt) fails the bar in the same run, isolating the goal/schema prompt as the driver (**PROMPT_ATTRIBUTED**) rather than a run-level environment artifact.

## 3. Falsifier

**H0.** No measurable treatment cell clears the bar — every COMPLETE M-7B-QWEN / M-3B-QWEN treatment cell has `task_success_rate < 0.6` — i.e. the goal/schema prompt does not convert the step-0 reveal-click into a full completion and the audited VF-01 failure mode (step-0 reveal click, re-click loop, zero answer actions) recurs under the enriched prompt. This is the Director's bounded negative: no factory-provisionable credential-free local CPU-quantized endpoint in the tested 3B–8B Qwen class can complete the minimal multi-step Web-agent task even with a properly specified goal/schema, so readiness condition (3) of the gated four-arm benchmark is not satisfied by this model class and the benchmark must be re-directed to hosted endpoints or a different model class.

FALSIFIES is asserted only over the COMPLETE, comparator-valid evaluated candidate set. A candidate whose treatment positive-control gate failed is recorded as `UNMEASURED_TREATMENT_PC_FAILED` / unresolved, not counted as a capability failure. A comparator cell that CLEARS the bar or drops below parseable 0.6 makes the prompt effect non-identifiable and the packet MEASUREMENT_INVALID (section 7, rule 2d); an EXCLUDED comparator invalidates only a clearing treatment (rule 2g) and is otherwise recorded as `COMP_UNANCHORED`.

## 4. Substrate, task and protocol

### 4.1 Frozen task and harness (inherited byte-for-byte)

The task, page fixture, GBNF grammar, user template, sampling schedule, seeds, model artifacts, parsing and scoring are inherited from `research/experiments/EXP-INTEL-37982024058/raw/harness_config.json` (file sha256 `7aba9dc899c40dd29f87b4265835eea6dc0b889c66271a983e4b82b8f5bc7adb`):

- Task: single page with a `#reveal-btn`; clicking it makes `#target` visible with text `TARGET-42`; the agent must click then answer `TARGET-42`. `task.max_steps_per_episode = 5`, `task.threshold_target_text = TARGET-42`.
- Frozen sampling: `temperature=0.0`, `max_tokens=512`, `n_ctx=2048`, `chat_format=qwen`, `llama_seed=42`, episodes seeded `base_seed(42) + episode_idx` ⇒ seeds 42–46. `n_threads=4`.
- Frozen parsing (parent `parse_action`): the whole completion must be valid JSON matching `{action: "click"|"answer", selector?: str, text?: str}` with the action-appropriate required field; any error/violation = parse failure.
- Frozen scorer (parent `run_episode`): mechanical reveal detection (`#target` visible with text `TARGET-42`) AND a terminal `answer` action whose text equals `TARGET-42` ⇒ `task_success=true`.
- Frozen clearing threshold: `task_success_rate_min = 0.6`, `parseable_action_rate_step1_min = 0.6`, `episodes = 5`.
- Frozen candidate table `candidate_models_frozen` with ids `M-7B-QWEN` (primary) and `M-3B-QWEN` (fallback).

### 4.2 The single manipulated variable: deterministic per-cell config overlay

For every cell we materialize a per-cell `raw/harness_config.json` by loading the frozen parent config (`7aba9dc8…`) and replacing **only** `prompts.system` with the condition string, frozen verbatim:

- `P-COMP-UNDERSPECIFIED` (comparator; byte-identical to the parent, string sha256 `1294954da7b1d6b9570b07e1e39cb48515b925355d0f33d5fabf72c8e8ce3876`):
  `You are a web agent. Reply with ONLY a valid JSON action per the schema. No prose, no reasoning, no markdown.`
- `P-TREAT-GOAL-SCHEMA` (treatment; sha256 `36a4240aba96e46797c16aebbedcc548778a0c1097b4ce4432608148758c5716`):
  `You are a web agent. Reply ONLY with one JSON object per turn, no prose. Actions available: {"action":"click","selector":"<id>"} or {"action":"answer","text":"<code>"}. Click the button to reveal the code, then answer it.`

Every other config key (`positive_control`, `null_control`, `random_baseline`, `clearing_threshold`, `gbnf_grammar`, `prompts.user_template`, `prompts.positive_control_probe`, `task`, `sampling`, `candidate_models_frozen`, `metrics_stable_ids`, `action_schema`) is inherited byte-for-byte from the frozen parent file. Materialized per-cell configs are:
`configs/config_<candidate_id>_<condition_id>.json` with deterministic names and sha256 recorded in `provenance.json`. EXECUTE must verify the byte-exact difference is confined to `prompts.system`.

Provenance of the treatment string: the grandparent SYS constant enumerates a goal and a `ref`→selector schema; the parent task's frozen GBNF admits only the keys `selector` and `text`, so the single alignment (`ref`→`selector`) makes the prompt's named schema match the grammar-enforced schema. The treatment adds exactly the two dimensions audit VF-01 says the parent prompt lacked: (a) enumeration of the action schema, (b) the task goal sentence. It does **not** contain the substrings `#reveal-btn` or `TARGET-42` (design-time verified), so a positive outcome cannot be attributed to answer leakage.

### 4.3 Cell orchestration and engine

Model cells are executed by the **frozen parent runner** `research/intel/run_exp_37982024058.py` (sha256 `2b5d5bb5da608adbcc68cc78120a88bc2b8809816e29f9d87d25c0c75bc25c00`), invoked once per cell:

```
python research/intel/run_exp_37982024058.py --mode probe-candidate \
  --outdir <per-cell-dir> --candidate <candidate_id> --gguf <pinned gguf paths...> \
  --chrome /usr/bin/google-chrome --n-threads 4
```

The per-cell dir contains the section-4.2 config. `mode_probe_candidate` runs the frozen `PC-JSON-CONSTRAINED-DECODING` gate, then (only if it passes) the 5 frozen seeded episodes against the served task page, writing `raw/model_receipts.json`. No new model-path or scoring code is authored.

The three mechanical controls (`PC-ORACLE-EPISODE`, `NC-NO-MODEL-ACTION`, `B-RANDOM-ACTION`) and the evaluator are provided by the thin driver specified in **Appendix A**. That driver must import the frozen parent primitives (`run_episode`, `make_null_producer`, `make_random_producer`, `parse_action`, `start_page_server`) rather than re-implement them, and must navigate the page to the served task URL before running any episode (repairing the parent's control defect, Appendix A.2).

Cell loop (per section 7): for each candidate in `[M-7B-QWEN, M-3B-QWEN]`, run the treatment cell and the comparator cell as a contemporaneous pair in one run. Comparator cells are collected unconditionally before any decision.

## 5. Measurements

Stable metric ids (parent ids preserved; one new metric defined here):

| id | definition | unit |
|---|---|---|
| `positive_control_pass_rate` | PC-JSON-CONSTRAINED-DECODING probes returning valid schema JSON / 10 | fraction |
| `parseable_action_rate_step1` | episodes whose step-0 completion passes frozen `parse_action` / 5 | fraction |
| `answer_action_emission_rate` | **new**: episodes emitting ≥1 terminal `answer` action with `parse_ok` / 5 | fraction |
| `task_success_rate` | episodes with `task_success=true` under the frozen scorer / 5 | fraction |
| `mean_inference_latency_s` | mean per-call latency over a cell's model calls | seconds |
| `mean_completion_tokens` | mean completion tokens over a cell's model calls | tokens |

`answer_action_emission_rate` is added because the parent reported only `task_success_rate`/`parseable_action_rate_step1` and its zero-answer fact had to be inferred from raw traces; it makes the VF-01 failure mode directly measurable. The parent's five ids are unchanged in meaning.

`metrics_stable_ids` in spec.json is the frozen identity list for EXECUTE/AUDIT.

## 6. Controls (stable ids)

- **PC-SUITE-EXP-INTEL-38164607941** (positive-control suite)
  - `PC-JSON-CONSTRAINED-DECODING`: 10 probes per cell (each candidate under both conditions) of the frozen probe string `Emit exactly: {"action":"click","selector":"#test"}` under the cell's own `prompts.system` with the frozen grammar. Success 10/10; a failing cell is EXCLUDED (no episodes).
  - `PC-ORACLE-EPISODE`: 5 scripted episodes (click `#reveal-btn`; answer `TARGET-42`) driven through the **real** frozen `run_episode` scorer against the served page. Success 5/5 `task_success=true`. Failure ⇒ preflight MEASUREMENT_INVALID.
- **NC-NO-MODEL-ACTION** (null control): 5 episodes of fixed non-JSON content `I will click the button` through the real scorer against the served page. Expected `parseable_action_rate_step1=0.0` AND `task_success_rate=0.0`; anything else ⇒ verification broken ⇒ MEASUREMENT_INVALID.
- **B-RANDOM-ACTION** (chance baseline): uniform action from the frozen 5-action space, 5 episodes, `random.Random(42)` created once and reused (as the parent does), run against the served page. Expected `parseable_action_rate_step1=1.0` (valid JSON by construction) and `task_success_rate < 0.6`. Analytic per-episode success probability is `sum_{j=1..4}(1/5)^(j+1) = 0.04992`, so `P(task_success_rate >= 3/5) = P(Binomial(5,0.04992) >= 3) ≈ 1.15e-3`; the bar is effectively unreachable by chance. Design-time seed-42 simulation realized `task_success_rate = 0.2` (descriptive only, **not** a brittle exact gate). If `task_success_rate >= 0.6` ⇒ MEASUREMENT_INVALID.
- **B-UNDERSPECIFIED-PROMPT-7B / B-UNDERSPECIFIED-PROMPT-3B**: the contemporaneous comparator cells (mark `M-*` under P-COMP-UNDERSPECIFIED), paired with their treatment cells. Frozen expected anchor from the parent: `task_success_rate=0.0`, `parseable_action_rate_step1=1.0`, zero answer actions. Exact match ⇒ `REPLICATION_ANCHOR_EXACT`; a bar-failing deviation with parseable ≥ 0.6 ⇒ `REPLICATION_ANCHOR_DRIFT` (validity note; contrast remains identifiable). A comparator that clears the bar or drops below parseable 0.6 is hard MEASUREMENT_INVALID (rule 2d); an EXCLUDED comparator is `COMP_UNANCHORED` and invalidates only a clearing treatment (rule 2g).
- **B-0.5B-QWEN-LOCAL**, **B-POLLINATIONS-PROXY**: carried reference baselines (not re-run).

Control-sensitivity repair: the parent's `mode_null_random` never navigates to the served page, so its random baseline ran against `about:blank` and its `task_success_rate=0.0` was structurally forced. This design runs all mechanical controls against the served page (Appendix A.2), so a positive is registerable and a null cannot be an artifact of broken navigation.

## 7. Decision rule (frozen)

`OUTCOME ∈ {SUPPORTS, FALSIFIES, MEASUREMENT_INVALID}`; `status=COMPLETE` unless operational blockers prevent every cell.

**Definitions.** A **cell** is one `(candidate, prompt-condition)` unit = PC-JSON gate (10 probes; passed iff `positive_control_pass_rate == 1.0`) + an episode batch (`clearing_threshold.episodes = 5`). A cell is **COMPLETE** iff its PC gate passed AND it recorded exactly 5 episode records; **EXCLUDED** iff its PC gate did not pass (no episodes run); **PARTIAL** iff its PC gate passed but it recorded fewer than 5 episode records; **CLEARS** iff COMPLETE and `task_success_rate >= 0.6` AND `parseable_action_rate_step1 >= 0.6`; a comparator cell is **VALID** iff COMPLETE and `task_success_rate < 0.6` AND `parseable_action_rate_step1 >= 0.6`; **CONFOUND** iff COMPLETE and (`task_success_rate >= 0.6` OR `parseable_action_rate_step1 < 0.6`).

Comparator validity is required for **attribution** of a treatment positive; it is descriptive (anchor replication) for a treatment negative, because FALSIFIES is a statement about the treatment cell alone and scorer liveness is guaranteed separately by preflight `PC-ORACLE-EPISODE`.

**Precedence (first matching rule wins).**

1. **PREFLIGHT.** `PC-ORACLE-EPISODE == 5/5` AND `NC-NO-MODEL-ACTION == (parseable 0.0, success 0.0)` AND `B-RANDOM-ACTION == (parseable 1.0, task_success_rate < 0.6)` AND all `freeze_artifact` hash checks match AND required stack imports OK AND GGUF digest checks PASS; else `OUTCOME=MEASUREMENT_INVALID`.
2. **CANDIDATE LOOP** over `[M-7B-QWEN, M-3B-QWEN]`, each candidate measured in one run:
   - 2a. Run the **TREAT** cell (PC gate then 5 episodes) and the **COMP** cell (PC gate then 5 episodes) unconditionally as a contemporaneous pair.
   - 2b. If the TREAT cell is EXCLUDED, the candidate yields no capability measurement: record `UNMEASURED_TREATMENT_PC_FAILED` and continue to the next candidate (unresolved, **not** a failure; its COMP disposition is recorded but does not gate other candidates).
   - 2c. If the TREAT cell is PARTIAL, or COMP is PARTIAL while TREAT is COMPLETE, a partial cell cannot decide a clearance or a confound ⇒ `OUTCOME=MEASUREMENT_INVALID`, STOP.
   - 2d. If the COMP cell is CONFOUND (`task_success_rate >= 0.6` OR `parseable_action_rate_step1 < 0.6`) ⇒ prompt effect not identifiable ⇒ `OUTCOME=MEASUREMENT_INVALID`, STOP.
   - 2e. Record the comparator disposition if COMP is COMPLETE-and-VALID: `task_success_rate=0.0`, `parseable_action_rate_step1=1.0`, zero answer actions ⇒ `REPLICATION_ANCHOR_EXACT`; any other VALID value ⇒ `REPLICATION_ANCHOR_DRIFT` (validity note); COMP EXCLUDED ⇒ `COMP_UNANCHORED` (validity note).
   - 2f. If the TREAT cell CLEARS **and** COMP is COMPLETE-and-VALID ⇒ `OUTCOME=SUPPORTS` (`PROMPT_ATTRIBUTED`), **STOP** (early stop on the first attributable clearing candidate).
   - 2g. If the TREAT cell CLEARS but COMP is EXCLUDED (`COMP_UNANCHORED`), a clearing treatment that cannot be contrasted against its contemporaneous anchor is unattributable ⇒ `OUTCOME=MEASUREMENT_INVALID`, STOP.
   - 2h. If the TREAT cell is COMPLETE but does not CLEAR, record the candidate as `TREATMENT_FAILS_BAR` and continue.
3. If at least one TREAT cell is COMPLETE and none CLEARED ⇒ `OUTCOME=FALSIFIES` (bounded negative over the evaluated COMPLETE treatment-cell set; any `COMP_UNANCHORED`/`DRIFT` dispositions are preserved as validity notes and do not block the treatment-level negative).
4. If no candidate produced a COMPLETE TREAT cell (all EXCLUDED or interrupted) ⇒ `OUTCOME=MEASUREMENT_INVALID`.

`status=COMPLETE` for SUPPORTS/FALSIFIES; `status=MEASUREMENT_INVALID` for the invalid branches. A treatment-cell PC failure is never encoded as a capability failure.

## 8. Validity threats and limitations

- **Bundled treatment (second-order attribution limit).** The treatment bundles (a) the goal sentence, (b) the action-schema enumeration, and (c) the grandparent's exact phrasing/wording. The contrast identified is therefore "the grandparent harness goal/schema system prompt vs the parent underspecified system prompt" — the Director's operational question — not a lexically minimal single-phrase edit. This design identifies the bundle's causal effect vs the underspecified comparator; it does not separate goal-only from schema-only, from phrasing, or from a generic longer-prompt effect. That decomposition is explicitly out of scope and is a limitation, not a confound for the Director's bundled goal/schema question.
- **Grammar admission vs parse acceptance.** The frozen GBNF admits any single-field object whose keys are `selector` or `text` independent of the `click`/`answer` action, so grammar-feasible completions include schema-mismatched objects the frozen `parse_action` rejects. Treatment liveness therefore rests on the empirically verified PC 10/10 and comparator 5/5 step-1 parseable behavior, and a treatment cell with `parseable_action_rate_step1 < 0.6` cannot clear the bar, so this residual cannot manufacture a false SUPPORTS.
- **Deterministic protocol / no variance.** `temperature=0.0` + fixed seeds produced 5/5 identical trace structures in the parent (audit VF-03). The 3/5 rule is the pre-declared adequacy rule for a capability gate, not a statistical threshold; no variance estimate is possible. n=5 per candidate and n=5 controls, per the frozen adequacy rule (audit VF-05).
- **Representation loss (audit VF-04).** State is a simplified text DOM (`PAGE_TEXT`, `ELEMENTS`, `HISTORY`), not a full accessibility tree; after the reveal `ELEMENTS` is empty and `PAGE_TEXT` contains `TARGET-42`. The parent assembly's re-click is therefore not attributable to missing page text; this design changes only the prompt and inherits the same representation.
- **Packaging deviation (audit VF-02).** The 7B frozen single-file URL is 404; the same-repo same-quant split shards are pinned and digest-verified. This is a provisioning/packaging deviation, not a model substitution.
- **Single task, single model family.** This is a capability gate on one minimal synthetic task in the Qwen 3B–8B class; clearing it is necessary but not sufficient for generality, and failing it does not close the Physics/other domains (this is `intel`, and the bounded negative is scoped to the tested class under this protocol).
- **Scorer scope.** Mechanical verification only (DOM + JSON schema); no LLM grading. The `#target` reveal and the terminal answer must both be observed by the frozen scorer.

## 9. Consequences

- **Positive (SUPPORTS, PROMPT_ATTRIBUTED).** The parent FALSIFIES is bounded to the underspecified-prompt ceiling; audit VF-01's prompt-underspecification hypothesis is confirmed as the driver; `C-LLM-INHERIT` readiness condition (3) is satisfied at mechanism level (a factory-provisionable credential-free programmatic endpoint can perform a minimal multi-step Web-agent task). The frozen four-arm benchmark (COLD vs INSTRUCTIONS vs RETRIEVAL vs SPIDER, same model/tools/budget) becomes executable with the verified goal/schema prompt as the in-prompt task specification, subject to the separate dynamic-range certificate for the comparator arms.
- **Negative (FALSIFIES, bounded).** The step-0-reveal re-click loop is NOT caused by missing instruction context at the 3B–8B Qwen class; the capability ceiling for credential-free CPU-quantized local models under this task/harness is real; readiness condition (3) is not satisfied by this model class; the credential-free path remains design-compromised. The recorded endpoint receipts (E-LOCAL-LLAMA, E-POLLINATIONS-OPENAI tokens/SLA) and the re-scope set (drop the same-model external published-baseline anchor in favor of internally re-run comparators on a dynamic-range task bank; or provision a hosted endpoint with pinning/SLA; or pursue a different model class) become decision inputs for the Global Research Director. This packet does not pre-decide the re-scope.
- **MEASUREMENT_INVALID.** No claim changes; the recorded repair must precede any re-run.

Whether `C-LLM-INHERIT` advances from HYPOTHESIS toward EXPERIMENTAL is a DIRECTOR adjudication, not a DESIGN/EXECUTE conclusion.

## 10. Prerequisites and satisfiability probes (design-time, non-outcome-bearing)

Design-time probes performed (allowed: cheap, non-outcome-bearing) and their results:

1. **Stack.** `python 3.12.15`, `pip 26.2.1`, `cmake 3.31.6`, `gcc/g++ 13.3.0` present; `/usr/bin/google-chrome` present; `nproc=4`; ~15 GB total RAM. `llama-cpp-python` and `playwright` are NOT preinstalled ⇒ EXECUTE installs/builds them. `llama-cpp-python==0.2.90` has a PyPI sdist and no cp312 wheel, so the build path is required and feasible (the parent built it).
2. **Grammar.** `raw/harness_config.json#gbnf_grammar` parsed rule-by-rule; all 7 rules (`root`, `ws`, `action`, `field`, `string`, `strchars`, `strchar`) defined and referenced; the parent constructed and executed it.
3. **URLs.** Via the confirmed `huggingface.co` resolve-redirect route: 3B 200, 7B split shard1 200, shard2 200, 7B single-file 404 (parent-documented). Digests pinned from `raw/gguf_sha256.txt`: 3B `626b4a66…` (2104932768 bytes); 7B shard1 `dfce12e3…` (3993201344 bytes), shard2 `539cf93f…` (689872288 bytes).
4. **Chance baseline.** Analytic and simulation results in section 6 (non-outcome-bearing).
5. **Runner contract.** Read the frozen parent runner: `mode_probe_candidate` reads `<outdir>/raw/harness_config.json` and uses `cfg["prompts"]["system"]`, `cfg["positive_control"]`, `cfg["clearing_threshold"]`, `cfg["task"]`; it navigates to the served page (line 379). `mode_null_random` starts the page server but never navigates to it — the documented control defect this design repairs (section 6, Appendix A.2).
6. **Sibling resume check.** EXP-INTEL-38123995594 has a complete spec (six checks PASS) but no `freeze.json`; its failure was the shared review-model outage. This packet preserves its control/metric identities and adds the two strengthenings recorded in `spec.comparative_reasoning`.

Provisioning plan: download the pinned GGUFs (digest-verified, fail-closed), build `llama-cpp-python==0.2.90`, install `playwright`, then run preflight controls.

## 11. Cost and information gain

CPU-only, up to 2 candidates × (1 comparator cell + 1 treatment cell) × (10 PC probes + up to 5 episodes × up to 5 steps) llama.cpp inferences. Parent per-call latency: 5.065 s (7B, 17 tok), 2.154 s (3B, 13 tok) ⇒ ~10–25 min inference worst case (early stop after the first clearing treatment cell). Provisioning ~20–45 min (≈6.8 GB GGUFs), `llama-cpp-python` build ~5–15 min, `playwright` <5 min, controls/preflight <5 min. No external API spend. Wall-clock estimate 45–150 min.

Information gain is high and decision-changing in both directions: it is the cheapest measurement that separates the two competing explanations audit VF-01/U-01/U-02 left open (prompt underspecification vs model capability/planning deficit) for the exact candidate pair at the exact frozen protocol, with within-run paired comparators and fail-closed preflight. SUPPORTS unblocks the flagship four-arm benchmark; FALSIFIES closes the credential-free local 3B–8B path as a capability result and hands the Director the receipts for a hosted-endpoint re-scope. It is readiness-condition-(3) work allocated by the CONTINUE mandate; it is not a census rerun and makes no economics/replay claim (P2-REPLAY-COST applies only downstream).

## 12. Inherited state from the parent handoff (four-way, preserved)

From EXP-INTEL-37982024058 handoff (sha256 `b2aee1ad…`):

- **established**: under the frozen underspecified-prompt protocol, no credential-free model cleared the bar (M-7B-QWEN 0/5, M-3B-QWEN 0/5; audit PASS); constrained decoding verified 10/10 both models; verification logic sound (NC 0/5 parseable/success, random 5/5 parseable/0/5 success); prompt-sensitive failure mode (step-0 reveal succeeds, then hidden-button re-click loop, no answer action).
- **rejected**: bounded to the frozen 3B–8B Qwen class under the frozen underspecified prompt (no general rejection of the credential-free path — prompt ablation needed); bounded to the frozen minimal synthetic task and Qwen family.
- **unknown**: whether the goal/schema prompt converts step-0 click to full completion (U-01) — this packet tests it; whether failure is general small-model planning or prompt-specific (U-02); whether 14B+/non-Qwen GGUFs clear the bar (U-03, out of scope); provisioning stability of the 7B split shards across repo revisions (U-04).
- **do_not_assume**: FALSIFIES is at the frozen protocol ceiling only; the 7B packaging deviated (same-model/quant shards used, not a substitution); the deterministic protocol has no variance estimate (3/5 is an adequacy rule, not statistics); the failure is not due to missing page text (VF-04); `C-LLM-INHERIT` remains HYPOTHESIS (not globally rejected).

## 13. Non-duplication

`spec.comparative_reasoning` records the LEGACY: NO_MATCH classification, the literal-search near-hits classified as NON-MATCHES, the nearest substantive precedents (P2-REPLAY-COST, P2-BLIND-COMPOSITION, P2-MIND2WEB) and why this probe is a distinct extension of the audited parent rather than a pre-2.0 repetition.

## 14. Freeze artifacts

Every mutable local code/data/fixture dependency whose identity can change the interpretation:

- `research/intel/run_exp_37982024058.py`
- `research/experiments/EXP-INTEL-37982024058/raw/harness_config.json`
- `research/experiments/EXP-INTEL-37973264582/raw/code/min_webagent.py`
- `research/experiments/EXP-INTEL-37982024058/raw/gguf_sha256.txt`
- `research/experiments/EXP-INTEL-37982024058/raw/provisioning_evidence.json`

All six `freeze_eligibility` checks are PASS with evidence refs in `spec.json`. The per-cell configs are deterministic transformations of the bound parent config (section 4.2) and therefore need no separate local file at freeze time; EXECUTE records their materialized sha256 in `provenance.json`. Remote GGUFs are frozen as URLs + digests, not bytes. `prereg.md` (this file) is hashed into `freeze.json`.

---

## Appendix A — controls & evaluator driver spec (thin, new, bounded)

The driver is the only new outcome-adjacent code. It must be minimal and must import, not re-implement, the frozen parent primitives.

**A.1 CLI.** `research/intel/exp_38164607941_controls.py` with a single mode `preflight-and-controls`:
`--outdir <dir> --config <per-cell-config> --chrome /usr/bin/google-chrome`.
It writes `raw/controls.json` (PC-ORACLE-EPISODE, NC-NO-MODEL-ACTION, B-RANDOM-ACTION records) and `raw/preflight.json`.

**A.2 Server + navigation repair.** Start the page server via the frozen `start_page_server(cfg["task"]["page_html"])`; launch Chromium with `executable_path=--chrome, headless=True, args=["--no-sandbox"]`; **explicitly `page.goto("http://127.0.0.1:<port>/")` before any episode** (repair of the parent's `mode_null_random` about:blank defect). `run_episode` re-navigates to `page.url`, so the served page persists across episodes.

**A.3 Imported frozen primitives (no reimplementation).** From `run_exp_37982024058.py`: `run_episode`, `make_null_producer`, `make_random_producer`, `start_page_server`, and (for sanity) `parse_action`. For PC-ORACLE-EPISODE the step producer is a fixed scripted producer returning `{"action":"click","selector":"#reveal-btn"}` on step 0 and `{"action":"answer","text":"TARGET-42"}` thereafter, fed through the real `run_episode`. For NC use `make_null_producer(cfg["null_control"]["fixed_invalid_content"])`. For B-RANDOM use `make_random_producer(cfg["random_baseline"]["action_space"], random.Random(cfg["sampling"]["base_seed"]))`.

**A.4 Preflight outputs.** `PC-ORACLE-EPISODE` = 5/5 `task_success`; `NC` = parseable 0.0 & success 0.0; `B-RANDOM` = parseable 1.0 & `task_success_rate < 0.6`. Any deviation ⇒ `preflight.json.pass=false` ⇒ section 7 rule 1.

**A.5 Evaluator.** `research/intel/exp_38164607941_eval.py` aggregates each cell's `raw/model_receipts.json` + the controls into `result.json` metrics/controls using the section-5 metric ids, computes the section-7 decision, and never inspects outcomes during DESIGN. It records raw evidence paths/hashes in `result.json.artifacts`.

Appendix A code is bound by this prereg; EXECUTE records its sha256 in `provenance.json`. Any deviation from Appendix A must be reported in `result.json.validity_notes`.

## Appendix B — design-time probe log (non-outcome-bearing)

| probe | result |
|---|---|
| Python/pip/cmake/gcc/Chrome/nproc/RAM | present as in section 10.1 |
| GBNF rule parse | 7/7 rules defined/referenced |
| 3B / 7B-shard1 / 7B-shard2 / 7B-single URL HEAD | 200 / 200 / 200 / 404 |
| Random-baseline analytic | p=0.04992; P(≥3/5)≈1.15e-3 |
| Random-baseline seed-42 simulation | task_success_rate=0.2 (descriptive) |
| Parent `mode_probe_candidate` navigation | serves page (line 379) |
| Parent `mode_null_random` navigation | about:blank defect confirmed |

No confirmatory or outcome-bearing measurement was run during DESIGN.
